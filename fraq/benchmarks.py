"""
Benchmark suite for fraq - compare with competitors.

Benchmarks:
- Generation speed (records/second)
- Memory usage (zero-storage advantage)
- Structural tests (fractal self-similarity vs random)

Results published in README and documentation.
"""

from __future__ import annotations

import gc
import time
import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class BenchmarkResult:
    """Single benchmark result."""
    name: str
    records: int
    time_seconds: float
    memory_bytes: int
    records_per_second: float


class SpeedBenchmark:
    """Benchmark generation speed."""
    
    @staticmethod
    def fraq_generate(count: int = 10000) -> BenchmarkResult:
        """Benchmark fraq generate()."""
        from fraq import generate
        
        gc.collect()
        start = time.perf_counter()
        
        records = generate({
            'id': 'str',
            'value': 'float:0-100',
            'active': 'bool',
        }, count=count)
        
        elapsed = time.perf_counter() - start
        
        return BenchmarkResult(
            name="fraq.generate()",
            records=count,
            time_seconds=elapsed,
            memory_bytes=0,  # Will be measured separately
            records_per_second=count / elapsed if elapsed > 0 else 0,
        )
    
    @staticmethod
    def fraq_stream(count: int = 10000) -> BenchmarkResult:
        """Benchmark fraq streaming (lazy)."""
        from fraq import stream
        
        gc.collect()
        start = time.perf_counter()
        
        records = []
        for record in stream({'value': 'float'}, count=count):
            records.append(record)
        
        elapsed = time.perf_counter() - start
        
        return BenchmarkResult(
            name="fraq.stream()",
            records=count,
            time_seconds=elapsed,
            memory_bytes=0,
            records_per_second=count / elapsed if elapsed > 0 else 0,
        )


class MemoryBenchmark:
    """Benchmark memory usage - fraq's zero-storage advantage."""
    
    @staticmethod
    def measure_memory_usage(
        generator_fn: Callable[[int], List[Dict]],
        count: int = 100000,
    ) -> int:
        """Measure peak memory usage during generation."""
        gc.collect()
        tracemalloc.start()
        
        _ = generator_fn(count)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return peak
    
    @staticmethod
    def compare_memory(count: int = 100000) -> Dict[str, int]:
        """Compare memory usage of different approaches."""
        results = {}
        
        # fraq generate
        def fraq_gen(n):
            from fraq import generate
            return generate({'value': 'float'}, count=n)
        
        results['fraq'] = MemoryBenchmark.measure_memory_usage(fraq_gen, count)
        
        # Faker (if available)
        try:
            from faker import Faker
            fake = Faker()
            
            def faker_gen(n):
                return [{'name': fake.name(), 'email': fake.email()} for _ in range(n)]
            
            results['faker'] = MemoryBenchmark.measure_memory_usage(faker_gen, count)
        except ImportError:
            results['faker'] = 0
        
        # Mimesis (if available)
        try:
            from mimesis import Person
            person = Person()
            
            def mimesis_gen(n):
                return [{'name': person.full_name()} for _ in range(n)]
            
            results['mimesis'] = MemoryBenchmark.measure_memory_usage(mimesis_gen, count)
        except ImportError:
            results['mimesis'] = 0
        
        return results


class StructuralBenchmark:
    """Benchmark fractal self-similarity vs random data."""
    
    @staticmethod
    def test_self_similarity(data: List[Dict[str, Any]], column: str = 'value') -> float:
        """Test if data has self-similar structure.
        
        Returns score 0.0-1.0 where 1.0 = perfect self-similarity.
        """
        from fraq.inference import FractalAnalyzer
        
        values = [row.get(column) for row in data if isinstance(row.get(column), (int, float))]
        if len(values) < 10:
            return 0.0
        
        analyzer = FractalAnalyzer()
        dim = analyzer.box_counting_dimension(values)
        
        # Fractal dimension between 1.0 and 1.8 indicates self-similarity
        if 1.0 <= dim.dimension <= 1.8:
            return dim.confidence
        return 0.0
    
    @staticmethod
    def compare_structures() -> Dict[str, float]:
        """Compare structural properties of different generators."""
        results = {}
        
        # fraq IFS
        from fraq.ifs import create_ifs
        ifs = create_ifs('organizational', seed=42)
        ifs_data = ifs.generate(count=1000, depth=3)
        results['fraq_ifs'] = StructuralBenchmark.test_self_similarity(ifs_data, 'fractal_value')
        
        # fraq generate (hash-based)
        from fraq import generate
        fraq_data = generate({'value': 'float'}, count=1000, seed=42)
        results['fraq_generate'] = StructuralBenchmark.test_self_similarity(fraq_data, 'value')
        
        # Faker random
        try:
            from faker import Faker
            fake = Faker()
            faker_data = [{'value': fake.random_int(0, 100)} for _ in range(1000)]
            results['faker'] = StructuralBenchmark.test_self_similarity(faker_data, 'value')
        except ImportError:
            results['faker'] = 0.0
        
        return results


def run_all_benchmarks(
    speed_count: int = 10000,
    memory_count: int = 100000,
) -> Dict[str, Any]:
    """Run all benchmarks and return results."""
    print("Running fraq benchmarks...")
    
    results = {
        'speed': {},
        'memory': {},
        'structure': {},
    }
    
    # Speed benchmarks
    print(f"\n1. Speed Benchmark (n={speed_count})")
    results['speed']['fraq_generate'] = SpeedBenchmark.fraq_generate(speed_count)
    results['speed']['fraq_stream'] = SpeedBenchmark.fraq_stream(speed_count)
    
    for name, result in results['speed'].items():
        print(f"   {name}: {result.records_per_second:,.0f} rec/s")
    
    # Memory benchmarks
    print(f"\n2. Memory Benchmark (n={memory_count})")
    results['memory'] = MemoryBenchmark.compare_memory(memory_count)
    
    for name, bytes_used in results['memory'].items():
        if bytes_used > 0:
            mb = bytes_used / (1024 * 1024)
            print(f"   {name}: {mb:.1f} MB")
    
    # Structural benchmarks
    print("\n3. Structural Benchmark (self-similarity)")
    results['structure'] = StructuralBenchmark.compare_structures()
    
    for name, score in results['structure'].items():
        print(f"   {name}: {score:.2f} (1.0 = perfect self-similarity)")
    
    return results


def _print_speed_section(data: Dict[str, BenchmarkResult]) -> None:
    """Print speed benchmark results. CC≤3"""
    if not data:
        return
    winner = max(data.items(), key=lambda x: x[1].records_per_second)
    print(f"\nFastest: {winner[0]} at {winner[1].records_per_second:,.0f} rec/s")


def _print_memory_section(data: Dict[str, int]) -> None:
    """Print memory benchmark results. CC≤3"""
    if not data or 'fraq' not in data:
        return
    fraq_mem = data['fraq']
    print(f"\nfraq memory: {fraq_mem / (1024*1024):.1f} MB")
    
    for name, mem in data.items():
        if name != 'fraq' and mem > 0:
            ratio = mem / fraq_mem if fraq_mem > 0 else 0
            print(f"{name}: {mem / (1024*1024):.1f} MB ({ratio:.1f}x fraq)")


def _print_structural_section(data: Dict[str, float]) -> None:
    """Print structural benchmark results. CC≤3"""
    if not data:
        return
    print("\nSelf-similarity scores:")
    for name, score in sorted(data.items(), key=lambda x: -x[1]):
        indicator = "✓" if score > 0.7 else " "
        print(f"  {indicator} {name}: {score:.2f}")


def print_summary(results: Dict[str, Any]) -> None:
    """Print benchmark summary. Orchestrator: CC≤3"""
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    
    _print_speed_section(results.get('speed', {}))
    _print_memory_section(results.get('memory', {}))
    _print_structural_section(results.get('structure', {}))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    results = run_all_benchmarks(speed_count=10000, memory_count=100000)
    print_summary(results)
