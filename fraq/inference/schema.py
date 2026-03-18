"""
Inferred schema for fractal data generation.

Schema inferred from real data with fractal properties.
CC target: ≤5 per function
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from fraq.inference.hierarchy import PatternSignature


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
        self._ifs = self._build_ifs()
    
    def _build_ifs(self) -> 'IFSGenerator':
        """Build IFS generator from detected patterns. CC≤4"""
        from fraq.ifs import IFSGenerator, AffineTransform
        
        transforms = []
        weights = []
        
        for pattern in self.patterns.values():
            scale = 1.0 / pattern.branching_factor
            trans = (pattern.similarity_score, 0.0, 0.0)
            transforms.append(AffineTransform(scale=scale, translation=trans))
            weights.append(pattern.similarity_score)
        
        if not transforms:
            transforms = [AffineTransform(scale=0.5, translation=(0.0,))]
            weights = [1.0]
        
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
        
        return IFSGenerator(transforms, weights)
    
    def _generate_value(
        self,
        coord: Tuple[float, ...],
        pattern: PatternSignature,
    ) -> Any:
        """Generate value for column based on pattern. CC≤4"""
        base = sum(c * c for c in coord) ** 0.5
        
        if pattern.pattern_type == 'self_similar':
            return base * (1.0 + pattern.depth * 0.1)
        elif pattern.pattern_type == 'periodic':
            return math.sin(base * 10) * pattern.branching_factor
        elif pattern.pattern_type == 'clustered':
            cluster = int(base * 5) * pattern.branching_factor
            return cluster + (base % 1.0)
        else:
            return base * pattern.branching_factor
    
    def generate(
        self,
        count: int = 100,
        seed: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Generate synthetic data with same fractal structure. CC≤4"""
        if seed is not None:
            self._ifs.rng.seed(seed)
        
        records = []
        for i in range(count):
            coord = self._ifs.generate_coordinate(depth=3)
            
            record = {"_index": i, "_coordinate": coord}
            
            for col, pattern in self.patterns.items():
                record[col] = self._generate_value(coord, pattern)
            
            records.append(record)
        
        return records
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary. CC≤3"""
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
