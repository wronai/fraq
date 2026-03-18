"""
Hierarchy detection for fractal pattern analysis.

Detects hierarchical structure in data columns.
CC target: ≤5 per function
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fraq.inference.dimension import BoxCountingAnalyzer, FractalDimension


class PatternSignature:
    """Detected pattern in data column."""
    
    def __init__(
        self,
        column: str,
        pattern_type: str,  # 'self_similar', 'periodic', 'random', 'clustered'
        depth: int,
        branching_factor: float,
        similarity_score: float,
    ):
        self.column = column
        self.pattern_type = pattern_type
        self.depth = depth
        self.branching_factor = branching_factor
        self.similarity_score = similarity_score


class HierarchyDetector:
    """Detect hierarchical patterns in data columns."""
    
    def __init__(self, min_depth: int = 2, max_depth: int = 6):
        self.min_depth = min_depth
        self.max_depth = max_depth
        self._dimension_analyzer = BoxCountingAnalyzer()
    
    def _extract_numeric_values(
        self,
        data: List[Dict[str, Any]],
        column: str,
    ) -> List[float]:
        """Extract numeric values from column. CC≤3"""
        if not data:
            return []
        
        values = []
        for row in data:
            val = row.get(column)
            if val is not None and isinstance(val, (int, float)):
                values.append(float(val))
        
        return values
    
    def _detect_pattern_type(self, dimension: FractalDimension) -> str:
        """Detect pattern type from dimension analysis. CC≤3"""
        if dimension.confidence > 0.7:
            return 'self_similar'
        elif dimension.dimension > 1.8:
            return 'clustered'
        elif dimension.dimension < 0.5:
            return 'periodic'
        else:
            return 'random'
    
    def _estimate_depth(self, values: List[float]) -> int:
        """Estimate recursion depth from value distribution. CC≤3"""
        if len(values) < 2:
            return self.min_depth
        
        unique_ratio = len(set(values)) / len(values)
        depth = int(1 / (unique_ratio + 0.1) * 2)
        
        return max(self.min_depth, min(self.max_depth, depth))
    
    def _estimate_branching(self, values: List[float]) -> float:
        """Estimate branching factor from distribution. CC≤3"""
        if len(values) < 2:
            return 2.0
        
        sorted_vals = sorted(values)
        diffs = [sorted_vals[i+1] - sorted_vals[i] for i in range(len(sorted_vals)-1)]
        avg_diff = sum(diffs) / len(diffs) if diffs else 1.0
        
        # Lower average diff = higher branching
        branching = 1.0 / (avg_diff + 0.1) * 2
        return min(10.0, max(2.0, branching))
    
    def detect(
        self,
        data: List[Dict[str, Any]],
        parent_column: Optional[str] = None,
    ) -> Dict[str, PatternSignature]:
        """Detect hierarchical structure in data. CC≤5"""
        patterns = {}
        
        if not data:
            return patterns
        
        columns = list(data[0].keys())
        
        for column in columns:
            # Extract values
            values = self._extract_numeric_values(data, column)
            
            if len(values) < 10:
                continue
            
            # Analyze dimension
            dim = self._dimension_analyzer.estimate(values)
            
            # Detect pattern type
            pattern_type = self._detect_pattern_type(dim)
            
            # Estimate parameters
            depth = self._estimate_depth(values)
            branching = self._estimate_branching(values)
            
            patterns[column] = PatternSignature(
                column=column,
                pattern_type=pattern_type,
                depth=depth,
                branching_factor=branching,
                similarity_score=dim.confidence,
            )
        
        return patterns
