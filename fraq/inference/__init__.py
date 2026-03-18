"""
Fractal Schema Inference - detect fractal patterns in existing data.

Refactored package structure - FractalAnalyzer is now a facade
delegating to specialized analyzers.

New structure:
- dimension.py: BoxCountingAnalyzer
- hierarchy.py: HierarchyDetector  
- correlation.py: CorrelationAnalyzer
- schema.py: InferredSchema

Example:
    from fraq.inference import infer_fractal, FractalAnalyzer
    
    # Using facade (backward compatible)
    analyzer = FractalAnalyzer()
    dim = analyzer.box_counting_dimension(values)
    
    # Using specialized analyzers directly
    from fraq.inference.dimension import BoxCountingAnalyzer
    dim = BoxCountingAnalyzer().estimate(values)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from fraq.inference.dimension import BoxCountingAnalyzer, FractalDimension
from fraq.inference.hierarchy import HierarchyDetector, PatternSignature
from fraq.inference.correlation import CorrelationAnalyzer
from fraq.inference.schema import InferredSchema


class FractalAnalyzer:
    """Facade delegating to specialized analyzers.
    
    Maintains backward compatibility while delegating
    to smaller, focused analyzer classes.
    """
    
    def __init__(self, min_depth: int = 2, max_depth: int = 6):
        self.min_depth = min_depth
        self.max_depth = max_depth
        self._box = BoxCountingAnalyzer()
        self._hier = HierarchyDetector(min_depth, max_depth)
        self._corr = CorrelationAnalyzer()
    
    def box_counting_dimension(
        self,
        values: List[float],
        min_box_size: float = None,
        max_box_size: float = None,
    ) -> FractalDimension:
        """Calculate box-counting dimension (delegated)."""
        return self._box.estimate(values, min_box_size, max_box_size)
    
    def detect_hierarchy(
        self,
        data: List[Dict[str, Any]],
        parent_column: Optional[str] = None,
    ) -> Dict[str, PatternSignature]:
        """Detect hierarchical structure (delegated)."""
        return self._hier.detect(data, parent_column)
    
    def analyze_correlations(
        self,
        data: List[Dict[str, Any]],
    ) -> Dict[Tuple[str, str], float]:
        """Analyze correlations (delegated)."""
        return self._corr.analyze(data)


def infer_fractal(
    data: List[Dict[str, Any]],
    min_depth: int = 2,
    max_depth: int = 6,
) -> InferredSchema:
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
    
    patterns = analyzer.detect_hierarchy(data)
    correlations = analyzer.analyze_correlations(data)
    
    return InferredSchema(
        patterns=patterns,
        correlations=correlations,
        sample_data=data[:10] if data else [],
    )


__all__ = [
    # Facade and main function
    'FractalAnalyzer',
    'infer_fractal',
    # Specialized analyzers
    'BoxCountingAnalyzer',
    'HierarchyDetector',
    'CorrelationAnalyzer',
    # Data classes
    'FractalDimension',
    'PatternSignature',
    'InferredSchema',
]
