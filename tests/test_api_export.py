"""Tests for API module - DataFrame export via generate()."""

import pytest
from fraq.api import generate, _to_polars, _to_pandas, _to_arrow


class TestGenerateOutput:
    """Test generate() with output parameter."""
    
    def test_output_list_default(self):
        """Test default output='list'."""
        records = generate({'value': 'float'}, count=5)
        assert isinstance(records, list)
        assert len(records) == 5
    
    def test_output_list_explicit(self):
        """Test explicit output='list'."""
        records = generate({'value': 'float'}, count=5, output='list')
        assert isinstance(records, list)
        assert len(records) == 5
    
    def test_output_records(self):
        """Test output='records' returns iterator."""
        result = generate({'value': 'float'}, count=5, output='records')
        # Should be an iterator
        records = list(result)
        assert len(records) == 5
    
    def test_output_invalid_raises(self):
        """Test that invalid output raises ValueError."""
        with pytest.raises(ValueError):
            generate({'value': 'float'}, count=5, output='invalid')


class TestPolarsExport:
    """Test Polars DataFrame export."""
    
    def test_import_error_without_polars(self):
        """Test that helpful ImportError is raised."""
        try:
            import polars
            pytest.skip("Polars is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError) as exc_info:
            generate({'value': 'float'}, count=5, output='polars')
        
        assert 'fraq[polars]' in str(exc_info.value)


class TestPandasExport:
    """Test Pandas DataFrame export."""
    
    def test_import_error_without_pandas(self):
        """Test that helpful ImportError is raised."""
        try:
            import pandas
            pytest.skip("Pandas is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError) as exc_info:
            generate({'value': 'float'}, count=5, output='pandas')
        
        assert 'fraq[pandas]' in str(exc_info.value)


class TestArrowExport:
    """Test PyArrow Table export."""
    
    def test_import_error_without_pyarrow(self):
        """Test that helpful ImportError is raised."""
        try:
            import pyarrow
            pytest.skip("PyArrow is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError) as exc_info:
            generate({'value': 'float'}, count=5, output='arrow')
        
        assert 'fraq[arrow]' in str(exc_info.value)


class TestFakerInGenerate:
    """Test Faker integration via generate()."""
    
    def test_faker_spec_raises_without_faker(self):
        """Test that faker spec raises ImportError without Faker."""
        try:
            import faker
            pytest.skip("Faker is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError):
            generate({'name': 'faker:name'}, count=5)


class TestConversionFunctions:
    """Test internal conversion functions."""
    
    def test_to_polars_empty(self):
        """Test _to_polars with empty records."""
        try:
            import polars as pl
            result = _to_polars([])
            assert isinstance(result, pl.DataFrame)
            assert len(result) == 0
        except ImportError:
            pytest.skip("Polars not installed")
    
    def test_to_pandas_empty(self):
        """Test _to_pandas with empty records."""
        try:
            import pandas as pd
            result = _to_pandas([])
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0
        except ImportError:
            pytest.skip("Pandas not installed")
    
    def test_to_arrow_empty(self):
        """Test _to_arrow with empty records."""
        try:
            import pyarrow as pa
            result = _to_arrow([])
            assert isinstance(result, pa.Table)
            assert result.num_rows == 0
        except ImportError:
            pytest.skip("PyArrow not installed")
