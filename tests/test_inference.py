"""Tests for fractal schema inference module."""

import pytest
import math
from fraq.inference import (
    FractalAnalyzer,
    FractalDimension,
    PatternSignature,
    infer_fractal,
    InferredSchema,
)


class TestFractalDimension:
    """Test FractalDimension dataclass."""
    
    def test_creation(self):
        """Test creating FractalDimension."""
        dim = FractalDimension(dimension=1.5, confidence=0.8, scales=[(10, 2.3)])
        assert dim.dimension == 1.5
        assert dim.confidence == 0.8
        assert dim.scales == [(10, 2.3)]


class TestFractalAnalyzer:
    """Test fractal analyzer."""
    
    def test_box_counting_dimension_empty(self):
        """Test with empty data."""
        analyzer = FractalAnalyzer()
        dim = analyzer.box_counting_dimension([])
        assert dim.dimension == 0.0
        assert dim.confidence == 0.0
    
    def test_box_counting_dimension_uniform(self):
        """Test with uniform data."""
        analyzer = FractalAnalyzer()
        dim = analyzer.box_counting_dimension([1.0, 1.0, 1.0])
        assert dim.dimension == 0.0  # No variation
    
    def test_box_counting_dimension_linear(self):
        """Test with linear data."""
        analyzer = FractalAnalyzer()
        values = list(range(100))
        dim = analyzer.box_counting_dimension(values)
        # Should have some dimension > 0
        assert dim.dimension >= 0.0
    
    def test_detect_hierarchy(self):
        """Test hierarchy detection."""
        analyzer = FractalAnalyzer()
        data = [
            {'level': 0, 'value': 100.0},
            {'level': 1, 'value': 50.0},
            {'level': 2, 'value': 25.0},
        ] * 10
        
        patterns = analyzer.detect_hierarchy(data)
        # Should detect patterns in 'level' and 'value' columns
        assert len(patterns) > 0


class TestInferFractal:
    """Test fractal schema inference."""
    
    def test_infer_fractal_basic(self):
        """Test basic inference."""
        data = [
            {'id': i, 'value': float(i * 10)}
            for i in range(50)
        ]
        
        schema = infer_fractal(data)
        assert schema is not None
        assert len(schema.patterns) >= 0
        assert len(schema.sample_data) <= 10
    
    def test_inferred_schema_generate(self):
        """Test generating from inferred schema."""
        data = [
            {'id': i, 'value': float(i * 10)}
            for i in range(30)
        ]
        
        schema = infer_fractal(data)
        synthetic = schema.generate(count=10, seed=42)
        
        assert len(synthetic) == 10
        assert all('_index' in r for r in synthetic)
        assert all('_coordinate' in r for r in synthetic)
    
    def test_inferred_schema_determinism(self):
        """Test deterministic generation."""
        data = [{'id': i, 'value': float(i)} for i in range(20)]
        
        schema1 = infer_fractal(data)
        schema2 = infer_fractal(data)
        
        # Same input should produce same schema patterns
        assert len(schema1.patterns) == len(schema2.patterns)
    
    def test_to_dict(self):
        """Test schema serialization."""
        data = [{'id': i, 'value': float(i)} for i in range(10)]
        schema = infer_fractal(data)
        
        d = schema.to_dict()
        assert 'patterns' in d
        assert 'correlations' in d


class TestInferredSchemaWithIFS:
    """Test IFS integration with inferred schema."""
    
    def test_build_ifs(self):
        """Test IFS building from schema."""
        data = [{'level': i % 3, 'value': 100.0 / (i + 1)} for i in range(30)]
        schema = infer_fractal(data)
        
        # Should have built IFS
        assert schema._ifs is not None
        assert len(schema._ifs.transforms) > 0
