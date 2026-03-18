"""
Correlation analyzer for fractal pattern detection.

Analyzes self-similar correlations between columns.
CC target: ≤5 per function
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


class CorrelationAnalyzer:
    """Analyze self-similar correlations between columns."""
    
    def _extract_numeric_column(
        self,
        data: List[Dict[str, Any]],
        column: str,
    ) -> List[float]:
        """Extract numeric values from column. CC≤3"""
        values = []
        for row in data:
            val = row.get(column)
            if isinstance(val, (int, float)):
                values.append(float(val))
        return values
    
    def _calculate_means(self, values: List[float]) -> Tuple[float, float]:
        """Calculate mean for single column (used for variance). CC≤2"""
        if not values:
            return 0.0, 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return mean, variance
    
    def _calculate_correlation(
        self,
        values1: List[float],
        values2: List[float],
    ) -> float:
        """Calculate Pearson correlation coefficient. CC≤3"""
        if len(values1) != len(values2) or len(values1) < 2:
            return 0.0
        
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        
        # Calculate numerator and denominator
        numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
        
        std1 = math.sqrt(sum((v - mean1) ** 2 for v in values1))
        std2 = math.sqrt(sum((v - mean2) ** 2 for v in values2))
        
        if std1 == 0 or std2 == 0:
            return 0.0
        
        return numerator / (std1 * std2)
    
    def analyze(
        self,
        data: List[Dict[str, Any]],
    ) -> Dict[Tuple[str, str], float]:
        """Analyze correlations between columns. CC≤4"""
        correlations = {}
        
        if not data:
            return correlations
        
        columns = list(data[0].keys())
        n_cols = len(columns)
        
        # Pre-extract all columns
        column_data = {}
        for col in columns:
            column_data[col] = self._extract_numeric_column(data, col)
        
        # Calculate correlations (upper triangle only)
        for i in range(n_cols):
            col1 = columns[i]
            values1 = column_data[col1]
            
            if len(values1) < 2:
                continue
            
            for j in range(i + 1, n_cols):
                col2 = columns[j]
                values2 = column_data[col2]
                
                if len(values2) < 2:
                    continue
                
                corr = self._calculate_correlation(values1, values2)
                correlations[(col1, col2)] = corr
        
        return correlations
