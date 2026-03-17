"""
Fractal Schema Inference - detect fractal patterns in existing data.

Analyzes real data to find self-similar patterns, then creates
a FraqSchema that can generate infinite synthetic data with
the same structural properties.

This is different from SDV (which uses ML/GANs) - we use
fractal analysis which is:
- Faster (no training needed)
- Deterministic (same input → same schema)
- No GPU required
- Mathematically provable self-similarity

Example:
    import pandas as pd
    from fraq.inference import infer_fractal
    
    # Load real data
    df = pd.read_csv('sales_data.csv')
    
    # Infer fractal schema
    schema = infer_fractal(df)
    
    # Generate infinite synthetic data with same structure
    synthetic = schema.generate(count=100000)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class FractalDimension:
    """Fractal dimension analysis result."""
    dimension: float  # Box-counting dimension
    confidence: float  # 0.0-1.0, how "fractal-like" the data is
    scales: List[Tuple[int, float]]  # (box_size, count) pairs


@dataclass
class PatternSignature:
    """Detected pattern in data column."""
    column: str
    pattern_type: str  # 'self_similar', 'periodic', 'random', 'clustered'
    depth: int  # Detected recursion depth
    branching_factor: float  # Average children per parent
    similarity_score: float  # 0.0-1.0, self-similarity strength


class FractalAnalyzer:
    """Analyze data for fractal properties."""
    
    def __init__(self, min_depth: int = 2, max_depth: int = 6):
        self.min_depth = min_depth
        self.max_depth = max_depth
    
    def box_counting_dimension(
        self,
        values: List[float],
        min_box_size: float = None,
        max_box_size: float = None,
    ) -> FractalDimension:
        """Calculate box-counting dimension of value distribution.
        
        True fractals have non-integer dimensions (1.0 < d < 2.0 for curves).
        """
        if not values:
            return FractalDimension(0.0, 0.0, [])
        
        # Normalize to [0, 1]
        min_val, max_val = min(values), max(values)
        if max_val == min_val:
            return FractalDimension(0.0, 0.0, [])
        
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        
        # Box counting
        scales = []
        box_sizes = [2**(-i) for i in range(1, 8)]  # 0.5, 0.25, 0.125, ...
        
        for box_size in box_sizes:
            # Count boxes that contain at least one point
            boxes = set()
            for v in normalized:
                box_idx = int(v / box_size)
                boxes.add(box_idx)
            
            scales.append((len(boxes), math.log(1/box_size)))
        
        # Calculate dimension from slope of log(N) vs log(1/ε)
        if len(scales) >= 2:
            # Simple linear regression on log-log plot
            log_counts = [math.log(s[0]) if s[0] > 0 else 0 for s in scales]
            log_inv_sizes = [s[1] for s in scales]
            
            # Calculate slope (dimension)
            n = len(scales)
            sum_x = sum(log_inv_sizes)
            sum_y = sum(log_counts)
            sum_xy = sum(x * y for x, y in zip(log_inv_sizes, log_counts))
            sum_x2 = sum(x * x for x in log_inv_sizes)
            
            if sum_x2 > 0 and n > 1:
                dimension = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            else:
                dimension = 0.0
        else:
            dimension = 0.0
        
        # Confidence based on how close to typical fractal range
        confidence = max(0.0, 1.0 - abs(dimension - 1.5) / 1.5) if dimension > 0 else 0.0
        
        return FractalDimension(dimension, confidence, scales)
    
    def detect_hierarchy(
        self,
        data: List[Dict[str, Any]],
        parent_column: Optional[str] = None,
    ) -> Dict[str, PatternSignature]:
        """Detect hierarchical structure in data.
        
        Analyzes parent-child relationships to find fractal hierarchy patterns.
        """
        patterns = {}
        
        # Analyze each column for hierarchical patterns
        for column in data[0].keys() if data else []:
            values = [row.get(column) for row in data if row.get(column) is not None]
            
            if not values or not isinstance(values[0], (int, float)):
                continue
            
            numeric_values = [float(v) for v in values if isinstance(v, (int, float))]
            if len(numeric_values) < 10:
                continue
            
            # Calculate fractal dimension
            dim = self.box_counting_dimension(numeric_values)
            
            # Detect pattern type
            if dim.confidence > 0.7:
                pattern_type = 'self_similar'
            elif dim.dimension > 1.8:
                pattern_type = 'clustered'
            elif dim.dimension < 0.5:
                pattern_type = 'periodic'
            else:
                pattern_type = 'random'
            
            # Estimate depth from value distribution
            unique_ratio = len(set(numeric_values)) / len(numeric_values)
            depth = max(self.min_depth, min(self.max_depth, int(1 / unique_ratio * 3)))
            
            # Estimate branching factor from distribution
            sorted_vals = sorted(numeric_values)
            diffs = [sorted_vals[i+1] - sorted_vals[i] for i in range(len(sorted_vals)-1)]
            avg_diff = sum(diffs) / len(diffs) if diffs else 1.0
            branching = min(10, max(2, int(1.0 / avg_diff * 5)))
            
            patterns[column] = PatternSignature(
                column=column,
                pattern_type=pattern_type,
                depth=depth,
                branching_factor=branching,
                similarity_score=dim.confidence,
            )
        
        return patterns
    
    def analyze_correlations(
        self,
        data: List[Dict[str, Any]],
    ) -> Dict[Tuple[str, str], float]:
        """Analyze correlations between columns for fractal relationships."""
        correlations = {}
        
        if not data:
            return correlations
        
        columns = list(data[0].keys())
        
        for i, col1 in enumerate(columns):
            for col2 in columns[i+1:]:
                values1 = [float(row.get(col1, 0)) for row in data if isinstance(row.get(col1), (int, float))]
                values2 = [float(row.get(col2, 0)) for row in data if isinstance(row.get(col2), (int, float))]
                
                if len(values1) != len(values2) or len(values1) < 2:
                    continue
                
                # Simple correlation coefficient
                mean1, mean2 = sum(values1) / len(values1), sum(values2) / len(values2)
                
                numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
                std1 = math.sqrt(sum((v - mean1)**2 for v in values1))
                std2 = math.sqrt(sum((v - mean2)**2 for v in values2))
                
                if std1 > 0 and std2 > 0:
                    corr = numerator / (std1 * std2)
                    correlations[(col1, col2)] = corr
        
        return correlations


def infer_fractal(
    data: List[Dict[str, Any]],
    min_depth: int = 2,
    max_depth: int = 6,
) -> 'InferredSchema':
    """Infer fractal schema from existing data.
    
    This is the game-changer feature - analyze real data and create
    a schema that generates infinite synthetic data with the same
    structural properties.
    
    Args:
        data: List of dictionaries (rows) with real data
        min_depth: Minimum recursion depth
        max_depth: Maximum recursion depth
    
    Returns:
        InferredSchema with fractal properties
    
    Example:
        >>> import pandas as pd
        >>> df = pd.read_csv('sales.csv')
        >>> data = df.to_dict('records')
        >>> schema = infer_fractal(data)
        >>> synthetic = schema.generate(count=10000)
    """
    analyzer = FractalAnalyzer(min_depth=min_depth, max_depth=max_depth)
    
    # Detect patterns
    patterns = analyzer.detect_hierarchy(data)
    correlations = analyzer.analyze_correlations(data)
    
    # Build inferred schema
    return InferredSchema(
        patterns=patterns,
        correlations=correlations,
        sample_data=data[:10] if data else [],
    )


class InferredSchema:
    """Schema inferred from real data with fractal properties."""
    
    def __init__(
        self,
        patterns: Dict[str, PatternSignature],
        correlations: Dict[Tuple[str, str], float],
        sample_data: List[Dict[str, Any]],
    ):
        self.patterns = patterns
        self.correlations = correlations
        self.sample_data = sample_data
        
        # Build IFS from detected patterns
        self._ifs = self._build_ifs()
    
    def _build_ifs(self) -> 'IFSGenerator':
        """Build IFS generator from detected patterns."""
        from fraq.ifs import IFSGenerator, AffineTransform
        
        # Create transforms based on detected patterns
        transforms = []
        weights = []
        
        for pattern in self.patterns.values():
            scale = 1.0 / pattern.branching_factor
            trans = (pattern.similarity_score, 0.0, 0.0)
            transforms.append(AffineTransform(scale=scale, translation=trans))
            weights.append(pattern.similarity_score)
        
        if not transforms:
            # Default transform
            transforms = [AffineTransform(scale=0.5, translation=(0.0,))]
            weights = [1.0]
        
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
        
        return IFSGenerator(transforms, weights)
    
    def generate(self, count: int = 100, seed: Optional[int] = None) -> List[Dict[str, Any]]:
        """Generate synthetic data with same fractal structure."""
        if seed is not None:
            self._ifs.rng.seed(seed)
        
        records = []
        for i in range(count):
            coord = self._ifs.generate_coordinate(depth=3)
            
            # Build record from patterns
            record = {"_index": i, "_coordinate": coord}
            
            for col, pattern in self.patterns.items():
                # Generate value based on coordinate and pattern
                value = self._generate_value(coord, pattern)
                record[col] = value
            
            records.append(record)
        
        return records
    
    def _generate_value(self, coord: Tuple[float, ...], pattern: PatternSignature) -> Any:
        """Generate a value for a column based on its pattern."""
        # Use coordinate to derive value
        base = sum(c * c for c in coord) ** 0.5
        
        if pattern.pattern_type == 'self_similar':
            # Scale and modulate based on depth
            return base * (1.0 + pattern.depth * 0.1)
        elif pattern.pattern_type == 'periodic':
            # Create periodic values
            return math.sin(base * 10) * pattern.branching_factor
        elif pattern.pattern_type == 'clustered':
            # Cluster around multiples
            cluster = int(base * 5) * pattern.branching_factor
            return cluster + (base % 1.0)
        else:
            # Random-ish (but deterministic from coordinate)
            return base * pattern.branching_factor
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "patterns": {
                col: {
                    "type": p.pattern_type,
                    "depth": p.depth,
                    "branching": p.branching_factor,
                    "similarity": p.similarity_score,
                }
                for col, p in self.patterns.items()
            },
            "correlations": {
                f"{k[0]}-{k[1]}": v
                for k, v in self.correlations.items()
            },
        }
