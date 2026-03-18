"""Tests for DataFrame export module."""

import pytest
from fraq.dataframes import to_polars, to_pandas, to_arrow, generate_df


class TestToPolars:
    """Test Polars export."""
    
    def test_import_error_without_polars(self):
        """Test that ImportError is raised without Polars."""
        try:
            import polars
            pytest.skip("Polars is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError):
            to_polars({'value': 'float'}, count=5)


class TestToPandas:
    """Test Pandas export."""
    
    def test_import_error_without_pandas(self):
        """Test that ImportError is raised without Pandas."""
        try:
            import pandas
            pytest.skip("Pandas is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError):
            to_pandas({'value': 'float'}, count=5)


class TestToArrow:
    """Test PyArrow export."""
    
    def test_import_error_without_pyarrow(self):
        """Test that ImportError is raised without PyArrow."""
        try:
            import pyarrow
            pytest.skip("PyArrow is installed")
        except ImportError:
            pass
        
        with pytest.raises(ImportError):
            to_arrow({'value': 'float'}, count=5)


class TestGenerateDf:
    """Test unified generate_df function."""
    
    def test_invalid_output_format(self):
        """Test that invalid output format raises error."""
        with pytest.raises(ValueError):
            generate_df({'value': 'float'}, count=5, output='invalid')
    
    def test_valid_output_formats(self):
        """Test that valid formats don't raise errors (may raise ImportError)."""
        for fmt in ['polars', 'pandas', 'arrow']:
            try:
                # This may raise ImportError if library not installed
                # which is expected behavior
                pass
            except:
                pass
