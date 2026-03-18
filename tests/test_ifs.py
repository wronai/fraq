"""Tests for IFS (Iterated Function System) generator."""

import pytest
from fraq.ifs import AffineTransform, IFSGenerator, create_ifs, OrganizationalMapper, NetworkMapper


class TestAffineTransform:
    """Test affine transformation."""
    
    def test_basic_transform(self):
        """Test basic scaling and translation."""
        transform = AffineTransform(scale=0.5, translation=(1.0,))
        result = transform.apply((2.0,))
        assert result == (2.0,)  # 0.5 * 2.0 + 1.0 = 2.0
    
    def test_multi_dimensional(self):
        """Test multi-dimensional transformation."""
        transform = AffineTransform(scale=0.5, translation=(1.0, 2.0))
        result = transform.apply((2.0, 4.0))
        assert result == (2.0, 4.0)


class TestIFSGenerator:
    """Test IFS generator."""
    
    def test_init(self):
        """Test IFS initialization."""
        transforms = [
            AffineTransform(scale=0.5),
            AffineTransform(scale=0.3),
        ]
        ifs = IFSGenerator(transforms, weights=[0.6, 0.4], seed=42)
        assert len(ifs.transforms) == 2
        assert len(ifs.weights) == 2
        assert abs(sum(ifs.weights) - 1.0) < 0.001  # Normalized
    
    def test_generate_coordinate(self):
        """Test coordinate generation."""
        transforms = [AffineTransform(scale=0.5)]
        ifs = IFSGenerator(transforms, seed=42)
        coord = ifs.generate_coordinate(depth=3)
        assert len(coord) == 3
        assert all(isinstance(c, float) for c in coord)
    
    def test_generate_records(self):
        """Test record generation."""
        transforms = [AffineTransform(scale=0.5)]
        ifs = IFSGenerator(transforms, seed=42)
        records = ifs.generate(count=10, depth=2)
        
        assert len(records) == 10
        assert all('_index' in r for r in records)
        assert all('_coordinate' in r for r in records)
        assert all('fractal_value' in r for r in records)
    
    def test_determinism(self):
        """Test deterministic generation with same seed."""
        transforms = [AffineTransform(scale=0.5)]
        ifs1 = IFSGenerator(transforms, seed=42)
        ifs2 = IFSGenerator(transforms, seed=42)
        
        records1 = ifs1.generate(count=5, depth=2)
        records2 = ifs2.generate(count=5, depth=2)
        
        for r1, r2 in zip(records1, records2):
            assert r1['fractal_value'] == r2['fractal_value']


class TestCreateIFS:
    """Test IFS factory function."""
    
    def test_organizational(self):
        """Test organizational pattern."""
        ifs = create_ifs('organizational', seed=42)
        assert len(ifs.transforms) == 3
        records = ifs.generate(count=5)
        assert len(records) == 5
    
    def test_network(self):
        """Test network pattern."""
        ifs = create_ifs('network', seed=42)
        assert len(ifs.transforms) == 2
        records = ifs.generate(count=5)
        assert len(records) == 5
    
    def test_generic(self):
        """Test generic pattern."""
        ifs = create_ifs('generic', seed=42)
        assert len(ifs.transforms) == 2
        records = ifs.generate(count=5)
        assert len(records) == 5


class TestOrganizationalMapper:
    """Test organizational data mapper."""
    
    def test_map_value(self):
        """Test value mapping."""
        mapper = OrganizationalMapper()
        value = mapper.map_value((0.5, 0.3, 0.2), depth=2)
        
        assert 'level' in value
        assert 'budget' in value
        assert 'headcount' in value
        assert value['level'] in ['department', 'team', 'individual']


class TestNetworkMapper:
    """Test network data mapper."""
    
    def test_map_value(self):
        """Test value mapping."""
        mapper = NetworkMapper()
        value = mapper.map_value((0.5, 0.3), depth=1)
        
        assert 'ip' in value
        assert 'latency_ms' in value
        assert 'bandwidth_mbps' in value
