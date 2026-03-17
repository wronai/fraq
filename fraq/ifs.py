"""
IFS (Iterated Function System) generator for fractal data.

This is fraq's unique advantage - true structural self-similarity
that competitors (Faker, Mimesis, SDV) cannot replicate.

The IFS generates data where level N has statistically similar structure
to level N+1, enabling:
- Testing recursive algorithms with guaranteed input structure
- Hierarchical organizational data with natural distribution
- Network tree simulations with repeating patterns

Example:
    from fraq.ifs import IFSGenerator, AffineTransform
    
    # Define transforms for organizational hierarchy
    transforms = [
        AffineTransform(scale=0.5, translation=(0, 0)),      # Department
        AffineTransform(scale=0.3, translation=(0.5, 0)),    # Team
        AffineTransform(scale=0.2, translation=(0.8, 0)),    # Individual
    ]
    
    ifs = IFSGenerator(transforms, weights=[0.4, 0.35, 0.25])
    org_data = ifs.generate(count=1000, depth=3)
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Optional, Protocol, Tuple


Vector = Tuple[float, ...]


@dataclass
class AffineTransform:
    """Affine transformation for IFS.
    
    Transforms a point in fractal space: x' = scale * x + translation
    """
    scale: float = 1.0
    translation: Vector = (0.0,)
    rotation: float = 0.0  # degrees
    
    def apply(self, point: Vector) -> Vector:
        """Apply transformation to a point."""
        # Simple scaling + translation
        # Rotation omitted for simplicity (can be added later)
        result = []
        for i, coord in enumerate(point):
            trans = self.translation[i] if i < len(self.translation) else 0.0
            result.append(self.scale * coord + trans)
        return tuple(result)


class ValueMapper(Protocol):
    """Protocol for mapping fractal coordinates to data values."""
    
    def map_value(self, coordinate: Vector, depth: int) -> Any:
        """Convert fractal coordinate to data value."""
        ...


class IFSGenerator:
    """Iterated Function System generator.
    
    Generates data with structural self-similarity - each zoom level
    has statistically similar properties to its parent.
    
    This is the core of fraq's unique advantage: true fractal structure
    in data generation, not just random or hashed values.
    """
    
    def __init__(
        self,
        transforms: List[AffineTransform],
        weights: Optional[List[float]] = None,
        seed: Optional[int] = None,
    ):
        """Initialize IFS with transforms and weights.
        
        Args:
            transforms: List of affine transformations
            weights: Probability weights for each transform (sums to 1.0)
            seed: Random seed for reproducibility
        """
        self.transforms = transforms
        self.weights = weights or [1.0 / len(transforms)] * len(transforms)
        self.rng = random.Random(seed)
        
        # Normalize weights
        total = sum(self.weights)
        self.weights = [w / total for w in self.weights]
    
    def _select_transform(self) -> AffineTransform:
        """Select transform based on weights."""
        r = self.rng.random()
        cumulative = 0.0
        for transform, weight in zip(self.transforms, self.weights):
            cumulative += weight
            if r <= cumulative:
                return transform
        return self.transforms[-1]  # Fallback
    
    def generate_coordinate(self, depth: int, start: Vector = (0.0, 0.0, 0.0)) -> Vector:
        """Generate a fractal coordinate at given depth.
        
        Applies transforms recursively to create self-similar structure.
        """
        point = start
        for _ in range(depth):
            transform = self._select_transform()
            point = transform.apply(point)
        return point
    
    def generate(
        self,
        count: int = 100,
        depth: int = 3,
        mapper: Optional[ValueMapper] = None,
    ) -> List[Dict[str, Any]]:
        """Generate records with fractal structure.
        
        Args:
            count: Number of records to generate
            depth: Fractal depth (hierarchy levels)
            mapper: Optional value mapper for custom data types
        
        Returns:
            List of records with self-similar structure
        """
        records = []
        for i in range(count):
            coord = self.generate_coordinate(depth)
            
            record = {
                "_index": i,
                "_depth": depth,
                "_coordinate": coord,
                "fractal_value": sum(c * c for c in coord) ** 0.5,  # Distance from origin
            }
            
            if mapper:
                record["value"] = mapper.map_value(coord, depth)
            
            records.append(record)
        
        return records
    
    def generate_hierarchy(
        self,
        root: Dict[str, Any],
        branching: List[int],
        depth: int = 3,
    ) -> Dict[str, Any]:
        """Generate hierarchical data (tree structure).
        
        Args:
            root: Root node data
            branching: Number of children per level [level0, level1, ...]
            depth: Maximum depth
        
        Returns:
            Root node with children recursively added
        """
        if depth <= 0:
            return root
        
        num_children = branching[0] if branching else 2
        children = []
        
        for i in range(num_children):
            # Generate child with IFS coordinate
            coord = self.generate_coordinate(depth)
            child = {
                "_index": i,
                "_coordinate": coord,
                "fractal_value": sum(c * c for c in coord) ** 0.5,
            }
            # Recursively add grandchildren
            grandchildren = self.generate_hierarchy(
                child,
                branching[1:] if len(branching) > 1 else [2],
                depth - 1,
            )
            if "children" in grandchildren:
                child["children"] = grandchildren["children"]
            children.append(child)
        
        root["children"] = children
        return root


class OrganizationalMapper(ValueMapper):
    """Mapper for organizational hierarchy data.
    
    Maps fractal coordinates to realistic organizational data:
    - Distance from origin → org level (dept, team, individual)
    - Coordinate values → budgets, headcounts, metrics
    """
    
    def __init__(
        self,
        levels: List[str] = None,
        budget_range: Tuple[float, float] = (10000, 1000000),
    ):
        self.levels = levels or ["department", "team", "individual"]
        self.budget_range = budget_range
    
    def map_value(self, coordinate: Vector, depth: int) -> Dict[str, Any]:
        """Map coordinate to organizational data."""
        level_idx = min(depth, len(self.levels) - 1)
        level = self.levels[level_idx]
        
        # Use coordinate to derive realistic values
        distance = sum(c * c for c in coordinate) ** 0.5
        budget = self.budget_range[0] + distance * (self.budget_range[1] - self.budget_range[0])
        
        return {
            "level": level,
            "budget": round(budget, 2),
            "headcount": max(1, int(50 / (depth + 1))),
            "coordinate": coordinate,
        }


class NetworkMapper(ValueMapper):
    """Mapper for network topology data.
    
    Maps fractal coordinates to network device properties.
    """
    
    def map_value(self, coordinate: Vector, depth: int) -> Dict[str, Any]:
        """Map coordinate to network data."""
        distance = sum(c * c for c in coordinate) ** 0.5
        
        # Derive IP-like address from coordinate
        ip_parts = [str(int(abs(c) * 255) % 256) for c in coordinate[:4]]
        ip = ".".join(ip_parts) if len(ip_parts) >= 4 else "192.168.1.1"
        
        return {
            "ip": ip,
            "latency_ms": round(distance * 100, 2),
            "bandwidth_mbps": max(10, int(1000 / (depth + 1))),
            "depth": depth,
        }


def create_ifs(
    pattern: str = "organizational",
    seed: Optional[int] = None,
) -> IFSGenerator:
    """Factory function to create pre-configured IFS generators.
    
    Args:
        pattern: Pattern type - 'organizational', 'network', 'generic'
        seed: Random seed
    
    Returns:
        Pre-configured IFSGenerator
    
    Example:
        >>> ifs = create_ifs("organizational", seed=42)
        >>> data = ifs.generate(count=100, depth=3)
    """
    if pattern == "organizational":
        transforms = [
            AffineTransform(scale=0.5, translation=(0.0, 0.0, 0.0)),
            AffineTransform(scale=0.3, translation=(0.5, 0.0, 0.0)),
            AffineTransform(scale=0.2, translation=(0.8, 0.0, 0.0)),
        ]
        weights = [0.3, 0.4, 0.3]
    elif pattern == "network":
        transforms = [
            AffineTransform(scale=0.6, translation=(0.0, 0.0)),
            AffineTransform(scale=0.4, translation=(0.4, 0.0)),
        ]
        weights = [0.5, 0.5]
    else:  # generic
        transforms = [
            AffineTransform(scale=0.5, translation=(0.0,)),
            AffineTransform(scale=0.5, translation=(0.5,)),
        ]
        weights = [0.5, 0.5]
    
    return IFSGenerator(transforms, weights, seed)
