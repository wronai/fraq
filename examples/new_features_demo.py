#!/usr/bin/env python3
"""Examples of new fraq features - Phase 2 & 3.

This file demonstrates:
- Faker integration (realistic data)
- DataFrame export (Polars/Pandas/Arrow)
- pytest fixtures
- IFS generator (fractal advantage)
- Fractal schema inference
"""

from __future__ import annotations


def example_1_faker():
    """Example 1: Generate realistic data with Faker."""
    print("=" * 60)
    print("Example 1: Faker Integration")
    print("=" * 60)
    
    try:
        from faker import Faker
        faker_available = True
    except ImportError:
        faker_available = False
        print("Faker not installed. Install with: pip install fraq[faker]")
        print("Skipping Faker example.")
        return
    
    from fraq import generate
    
    # Generate realistic Polish business data
    records = generate({
        'company_name': 'faker:pl_PL.company',
        'nip': 'faker:pl_PL.nip',
        'city': 'faker:pl_PL.city',
        'revenue': 'float:10000-1000000',
        'employees': 'int:5-500',
    }, count=5, seed=42)
    
    print(f"Generated {len(records)} Polish companies:")
    for r in records[:3]:
        print(f"  {r['company_name'][:30]:30} | NIP: {r['nip']} | {r['city']}")


def example_2_dataframes():
    """Example 2: Export to DataFrames."""
    print("\n" + "=" * 60)
    print("Example 2: DataFrame Export")
    print("=" * 60)
    
    try:
        from fraq.dataframes import to_polars
        
        df = to_polars({
            'sensor_id': 'str',
            'temperature': 'float:10-40',
            'humidity': 'float:0-100',
            'pressure': 'float:980-1060',
        }, count=1000, seed=42)
        
        print(f"Polars DataFrame: {len(df)} rows")
        print(f"Columns: {df.columns}")
        print(f"Mean temperature: {df['temperature'].mean():.1f}°C")
        
    except ImportError:
        print("Polars not installed. Install with: pip install fraq[polars]")


def example_3_pytest_fixture():
    """Example 3: pytest fixtures."""
    print("\n" + "=" * 60)
    print("Example 3: pytest Fixtures (simulated)")
    print("=" * 60)
    
    from fraq.testing import fraq_fixture
    
    # Simulating pytest fixture usage
    test_data = fraq_fixture({
        'user_id': 'str',
        'age': 'int:18-70',
        'active': 'bool',
    }, count=50, seed=42)
    
    print(f"Test data: {len(test_data)} users")
    
    # Simulate test assertions
    ages = [r['age'] for r in test_data]
    assert all(18 <= age <= 70 for age in ages), "All ages should be 18-70"
    print(f"  ✓ All ages in valid range (18-70)")
    
    actives = sum(1 for r in test_data if r['active'])
    print(f"  ✓ {actives} active users, {len(test_data) - actives} inactive")


def example_4_ifs_generator():
    """Example 4: IFS Generator - true fractal data."""
    print("\n" + "=" * 60)
    print("Example 4: IFS Generator (Fractal Advantage)")
    print("=" * 60)
    
    from fraq.ifs import create_ifs, OrganizationalMapper
    
    # Create organizational hierarchy with fractal structure
    ifs = create_ifs('organizational', seed=42)
    
    # Generate hierarchical data
    data = ifs.generate(
        count=10,
        depth=3,
        mapper=OrganizationalMapper(),
    )
    
    print(f"Generated {len(data)} organizational nodes:")
    for r in data[:3]:
        value = r.get('value', {})
        print(f"  Level: {value.get('level', 'N/A'):12} | "
              f"Budget: ${value.get('budget', 0):,.0f} | "
              f"Headcount: {value.get('headcount', 0)}")


def example_5_fractal_inference():
    """Example 5: Infer fractal schema from real data."""
    print("\n" + "=" * 60)
    print("Example 5: Fractal Schema Inference")
    print("=" * 60)
    
    from fraq.inference import infer_fractal
    
    # Simulate real hierarchical data (e.g., from database)
    real_data = []
    for i in range(50):
        level = i % 3  # 3 levels of hierarchy
        value = 1000 / (level + 1) + (i * 10) % 50
        real_data.append({
            'id': i,
            'level': level,
            'value': value,
            'budget': value * 10,
        })
    
    print(f"Real data: {len(real_data)} records with {len(set(r['level'] for r in real_data))} levels")
    
    # Infer fractal schema
    schema = infer_fractal(real_data)
    
    print(f"Detected patterns: {len(schema.patterns)}")
    for col, pattern in schema.patterns.items():
        print(f"  Column '{col}': {pattern.pattern_type} (similarity: {pattern.similarity_score:.2f})")
    
    # Generate synthetic data with same structure
    synthetic = schema.generate(count=5, seed=42)
    print(f"\nSynthetic data sample:")
    for r in synthetic[:2]:
        print(f"  {r}")


def example_6_benchmarks():
    """Example 6: Run benchmarks."""
    print("\n" + "=" * 60)
    print("Example 6: Performance Benchmarks")
    print("=" * 60)
    
    from fraq.benchmarks import SpeedBenchmark, MemoryBenchmark
    
    # Speed benchmark
    print("Running speed benchmark (n=1000)...")
    result = SpeedBenchmark.fraq_generate(1000)
    print(f"  Speed: {result.records_per_second:,.0f} records/second")
    
    # Memory benchmark (small scale for demo)
    print("\nRunning memory benchmark (n=10000)...")
    try:
        from fraq import generate
        def gen(n):
            return generate({'value': 'float'}, count=n)
        
        mem = MemoryBenchmark.measure_memory_usage(gen, 10000)
        print(f"  Memory: {mem / (1024*1024):.1f} MB")
    except Exception as e:
        print(f"  Skipped: {e}")


if __name__ == "__main__":
    example_1_faker()
    example_2_dataframes()
    example_3_pytest_fixture()
    example_4_ifs_generator()
    example_5_fractal_inference()
    example_6_benchmarks()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nInstall extras for full functionality:")
    print("  pip install fraq[faker,polars,pandas,arrow]")
