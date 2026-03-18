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

Plugin auto-discovery:
    pytest --fixtures | grep fraq
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def fraq_fixture(
    fields: Dict[str, str],
    count: int = 100,
    seed: int = 42,
    name: Optional[str] = None,
    output: str = "list",
) -> Any:
    """Generate deterministic test data as a fixture.
    
    This function creates reproducible test data with a fixed seed.
    Use in pytest fixtures for deterministic tests.
    
    Args:
        fields: Field specifications (same as generate())
        count: Number of records to generate
        seed: Random seed for reproducibility (default: 42)
        name: Optional fixture name (for documentation)
        output: Output format: 'list', 'polars', 'pandas', 'arrow'
    
    Returns:
        List of record dictionaries or DataFrame
    
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
        
        >>> # With DataFrame output
        >>> @pytest.fixture
        >>> def users_df():
        ...     return fraq_fixture({
        ...         'user_id': 'str',
        ...         'age': 'int:18-70',
        ...     }, count=50, seed=42, output='polars')
    """
    from fraq import generate
    return generate(fields, count=count, seed=seed, output=output)


def fixture_factory(
    fields: Dict[str, str],
    count: int = 100,
    seed: int = 42,
    output: str = "list",
) -> Callable[[F], F]:
    """Decorator to create pytest fixtures from fraq specs.
    
    Args:
        fields: Field specifications
        count: Number of records
        seed: Random seed
        output: Output format
    
    Returns:
        Decorator that creates pytest fixture
    
    Example:
        >>> from fraq.testing import fixture_factory
        >>>
        >>> @fixture_factory({
        ...     'temperature': 'float:10-40',
        ...     'humidity': 'float:0-100',
        ... }, count=100, seed=42)
        >>> def sensor_data():
        ...     pass  # Fixture created automatically
        >>>
        >>> def test_sensors(sensor_data):
        ...     assert len(sensor_data) == 100
    """
    def decorator(func: F) -> F:
        def wrapper():
            return fraq_fixture(fields, count=count, seed=seed, output=output)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__ or f"Fraq fixture: {fields}"
        return wrapper
    return decorator


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
        """Session-scoped fixture providing fraq utilities.
        
        Auto-discovered by pytest via entry point.
        """
        return {
            'generate': fraq_fixture,
            'make_fixture': make_fixture,
            'fixture_factory': fixture_factory,
        }
    
    @pytest.fixture(scope="function")
    def fraq_data():
        """Function-scoped fixture for generating test data.
        
        Usage:
            def test_example(fraq_data):
                data = fraq_data({
                    'value': 'float:0-100',
                }, count=10)
                assert len(data) == 10
        """
        def _generate(**kwargs):
            return fraq_fixture(**kwargs)
        return _generate
    
    @pytest.fixture(scope="function")
    def fraq_schema():
        """Function-scoped fixture providing schema utilities.
        
        Usage:
            def test_with_schema(fraq_schema):
                schema = fraq_schema({
                    'temp': 'float',
                    'id': 'str',
                })
                records = list(schema.records(count=5))
        """
        from fraq.core import FraqSchema, FraqNode
        def _schema(fields, seed=42):
            root = FraqNode(position=(0.0, 0.0, 0.0), seed=seed)
            schema = FraqSchema(root=root)
            for name, type_spec in fields.items():
                schema.add_field(name, type_spec)
            return schema
        return _schema
    
    # Auto-discovered fixtures
    FRAQ_FIXTURES = ['fraq_session', 'fraq_data', 'fraq_schema']
    
except ImportError:
    # pytest not installed, skip plugin registration
    pytest = None
    FRAQ_FIXTURES = []


__all__ = [
    'fraq_fixture',
    'make_fixture',
    'fixture_factory',
]

if pytest:
    __all__.extend(['fraq_session', 'fraq_data', 'fraq_schema'])
