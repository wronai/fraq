"""
pytest integration for fraq - fixtures and test utilities.

Provides pytest fixtures for easy test data generation.

Example:
    # conftest.py
    from fraq.testing import fraq_fixture
    
    @pytest.fixture
    def sensor_data():
        return fraq_fixture({
            'temperature': 'float:10-40',
            'sensor_id': 'str',
        }, count=100, seed=42)
    
    # test_sensors.py
    def test_temperature_range(sensor_data):
        assert all(10 <= r['temperature'] <= 40 for r in sensor_data)
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


def fraq_fixture(
    fields: Dict[str, str],
    count: int = 100,
    seed: int = 42,
    name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Generate deterministic test data as a fixture.
    
    This function creates reproducible test data with a fixed seed.
    Use in pytest fixtures for deterministic tests.
    
    Args:
        fields: Field specifications (same as generate())
        count: Number of records to generate
        seed: Random seed for reproducibility (default: 42)
        name: Optional fixture name (for documentation)
    
    Returns:
        List of record dictionaries
    
    Example:
        >>> # In conftest.py
        >>> import pytest
        >>> from fraq.testing import fraq_fixture
        >>> 
        >>> @pytest.fixture
        >>> def users():
        ...     return fraq_fixture({
        ...         'user_id': 'str',
        ...         'age': 'int:18-70',
        ...         'email': 'faker:email',
        ...     }, count=50, seed=42)
        >>>
        >>> # In test_users.py
        >>> def test_user_count(users):
        ...     assert len(users) == 50
        ...     assert all(18 <= u['age'] <= 70 for u in users)
    """
    from fraq import generate
    return generate(fields, count=count, seed=seed)


def make_fixture(
    fields: Dict[str, str],
    count: int = 100,
    seed: int = 42,
) -> Callable[[], List[Dict[str, Any]]]:
    """Create a fixture factory function.
    
    Returns a function that generates test data when called.
    Useful for creating parameterized fixtures.
    
    Args:
        fields: Field specifications
        count: Number of records
        seed: Random seed
    
    Returns:
        Function that returns test data
    
    Example:
        >>> # In conftest.py
        >>> sensor_factory = make_fixture({
        ...     'temperature': 'float:10-40',
        ...     'humidity': 'float:0-100',
        ... }, count=100)
        >>> 
        >>> @pytest.fixture
        >>> def sensors():
        ...     return sensor_factory()
        >>> 
        >>> @pytest.fixture
        >>> def more_sensors():
        ...     return sensor_factory(count=500)
    """
    def _factory(count_override: Optional[int] = None) -> List[Dict[str, Any]]:
        from fraq import generate
        return generate(fields, count=count_override or count, seed=seed)
    
    return _factory


# pytest plugin integration
try:
    import pytest
    
    @pytest.fixture(scope="session")
    def fraq_session():
        """Session-scoped fixture providing fraq utilities."""
        return {
            'generate': fraq_fixture,
            'make_fixture': make_fixture,
        }
    
    # Auto-discovered fixtures
    FRAQ_FIXTURES = ['fraq_session']
    
except ImportError:
    # pytest not installed, skip plugin registration
    pytest = None
    FRAQ_FIXTURES = []


__all__ = [
    'fraq_fixture',
    'make_fixture',
]

if pytest:
    __all__.append('fraq_session')
