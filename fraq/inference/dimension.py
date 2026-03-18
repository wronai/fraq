"""
Box-counting fractal dimension analyzer.

Isolated module for calculating fractal dimension using box-counting method.
CC target: ≤5 per function
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FractalDimension:
    """Fractal dimension analysis result."""
    dimension: float  # Box-counting dimension
    confidence: float  # 0.0-1.0, how "fractal-like" the data is
    scales: List[Tuple[int, float]]  # (box_size, count) pairs


class BoxCountingAnalyzer:
    """Isolated box-counting fractal dimension estimator."""
    
    def __init__(self, min_box_exp: int = 1, max_box_exp: int = 8):
        self.min_box_exp = min_box_exp
        self.max_box_exp = max_box_exp
    
    def _validate_values(self, values: List[float]) -> List[float]:
        """Clean and validate input. CC≤3"""
        if not values:
            return []
        
        # Filter non-numeric
        numeric = [float(v) for v in values if isinstance(v, (int, float))]
        if len(numeric) < 2:
            return []
        
        return numeric
    
    def _normalize(self, values: List[float]) -> Tuple[List[float], float, float]:
        """Normalize values to [0, 1] range. CC≤3"""
        min_val, max_val = min(values), max(values)
        
        if max_val == min_val:
            return [], 0.0, 0.0
        
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        return normalized, min_val, max_val
    
    def _count_boxes(self, values: List[float], box_size: float) -> int:
        """Count boxes that contain at least one point. CC≤3"""
        boxes = set()
        for v in values:
            box_idx = int(v / box_size)
            boxes.add(box_idx)
        return len(boxes)
    
    def _compute_scales(self, values: List[float]) -> List[Tuple[int, float]]:
        """Count boxes at each scale. CC≤3"""
        box_sizes = [2**(-i) for i in range(self.min_box_exp, self.max_box_exp)]
        scales = []
        
        for box_size in box_sizes:
            count = self._count_boxes(values, box_size)
            if count > 0:
                scales.append((count, math.log(1 / box_size)))
        
        return scales
    
    def _fit_dimension(self, scales: List[Tuple[int, float]]) -> float:
        """Linear regression to estimate dimension. CC≤2"""
        if len(scales) < 2:
            return 0.0
        
        log_counts = [math.log(s[0]) for s in scales]
        log_inv_sizes = [s[1] for s in scales]
        
        n = len(scales)
        sum_x = sum(log_inv_sizes)
        sum_y = sum(log_counts)
        sum_xy = sum(x * y for x, y in zip(log_inv_sizes, log_counts))
        sum_x2 = sum(x * x for x in log_inv_sizes)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator <= 0:
            return 0.0
        
        dimension = (n * sum_xy - sum_x * sum_y) / denominator
        return max(0.0, min(2.0, dimension))  # Clamp to valid range
    
    def _calculate_confidence(self, dimension: float) -> float:
        """Calculate confidence based on fractal range. CC≤2"""
        if dimension <= 0:
            return 0.0
        # Typical fractals have dimension between 0.5 and 1.5
        return max(0.0, 1.0 - abs(dimension - 1.0))
    
    def estimate(
        self,
        values: List[float],
        min_box_size: float = None,
        max_box_size: float = None,
    ) -> FractalDimension:
        """Orchestrate: validate → normalize → compute → fit. CC≤3"""
        # Validate
        clean_values = self._validate_values(values)
        if not clean_values:
            return FractalDimension(0.0, 0.0, [])
        
        # Normalize
        normalized, min_val, max_val = self._normalize(clean_values)
        if not normalized:
            return FractalDimension(0.0, 0.0, [])
        
        # Compute scales
        scales = self._compute_scales(normalized)
        if len(scales) < 2:
            return FractalDimension(0.0, 0.0, [])
        
        # Fit dimension
        dimension = self._fit_dimension(scales)
        confidence = self._calculate_confidence(dimension)
        
        return FractalDimension(dimension, confidence, scales)
