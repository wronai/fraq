"""Tests for testing module (pytest integration)."""

import pytest
from fraq.testing import fraq_fixture, make_fixture, fixture_factory


class TestFraqFixture:
    """Test fraq_fixture function."""
    
    def test_basic_usage(self):
        """Test basic fixture generation."""
        data = fraq_fixture({
            'id': 'str',
            'value': 'float:0-100',
        }, count=10, seed=42)
        
        assert len(data) == 10
        assert all('id' in r for r in data)
        assert all('value' in r for r in data)
    
    def test_default_seed(self):
        """Test that default seed is 42."""
        data1 = fraq_fixture({'value': 'float'}, count=5)
        data2 = fraq_fixture({'value': 'float'}, count=5)
        
        # Both should use seed=42 by default
        assert len(data1) == len(data2)
    
    def test_determinism(self):
        """Test deterministic generation."""
        data1 = fraq_fixture({'value': 'float'}, count=5, seed=123)
        data2 = fraq_fixture({'value': 'float'}, count=5, seed=123)
        
        assert len(data1) == len(data2)
        for r1, r2 in zip(data1, data2):
            assert r1['value'] == r2['value']
    
    def test_different_seeds(self):
        """Test that different seeds produce different data."""
        data1 = fraq_fixture({'value': 'float'}, count=5, seed=1)
        data2 = fraq_fixture({'value': 'float'}, count=5, seed=2)
        
        # Values should differ
        assert any(r1['value'] != r2['value'] for r1, r2 in zip(data1, data2))

    def test_output_parameter(self):
        """Test output parameter for DataFrame export."""
        # Test list output (default)
        data = fraq_fixture({'value': 'float'}, count=5, output='list')
        assert isinstance(data, list)
        
        # Test records output
        records = fraq_fixture({'value': 'float'}, count=5, output='records')
        assert hasattr(records, '__iter__')


class TestMakeFixture:
    """Test make_fixture factory function."""
    
    def test_factory_creation(self):
        """Test creating fixture factory."""
        factory = make_fixture({'value': 'float'}, count=10, seed=42)
        assert callable(factory)
    
    def test_factory_call(self):
        """Test calling factory function."""
        factory = make_fixture({'value': 'float'}, count=10, seed=42)
        data = factory()
        
        assert len(data) == 10
        assert all('value' in r for r in data)
    
    def test_factory_override_count(self):
        """Test overriding count in factory call."""
        factory = make_fixture({'value': 'float'}, count=10, seed=42)
        data = factory(20)  # Override count
        
        assert len(data) == 20


class TestFixtureFactory:
    """Test fixture_factory decorator."""
    
    def test_decorator_creates_callable(self):
        """Test that decorator creates callable."""
        @fixture_factory({'id': 'str'}, count=5, seed=42)
        def my_fixture():
            pass
        
        assert callable(my_fixture)
    
    def test_decorator_returns_data(self):
        """Test that decorated function returns fraq data."""
        @fixture_factory({'id': 'str'}, count=5, seed=42)
        def my_fixture():
            pass
        
        data = my_fixture()
        assert len(data) == 5
        assert all('id' in r for r in data)
    
    def test_decorator_preserves_name(self):
        """Test that decorator preserves function name."""
        @fixture_factory({'value': 'float'}, count=3, seed=42)
        def my_custom_fixture():
            """My docstring."""
            pass
        
        assert my_custom_fixture.__name__ == 'my_custom_fixture'
        assert my_custom_fixture.__doc__ == 'My docstring.'


class TestPytestPluginFixtures:
    """Test auto-discovered pytest fixtures."""
    
    def test_fraq_session_fixture_available(self):
        """Test that fraq_session fixture is available."""
        try:
            import pytest
            from fraq.testing import FRAQ_FIXTURES
            assert 'fraq_session' in FRAQ_FIXTURES
        except ImportError:
            pytest.skip("pytest not installed")
    
    def test_fraq_data_fixture_available(self):
        """Test that fraq_data fixture is available."""
        try:
            import pytest
            from fraq.testing import FRAQ_FIXTURES
            assert 'fraq_data' in FRAQ_FIXTURES
        except ImportError:
            pytest.skip("pytest not installed")
    
    def test_fraq_schema_fixture_available(self):
        """Test that fraq_schema fixture is available."""
        try:
            import pytest
            from fraq.testing import FRAQ_FIXTURES
            assert 'fraq_schema' in FRAQ_FIXTURES
        except ImportError:
            pytest.skip("pytest not installed")
