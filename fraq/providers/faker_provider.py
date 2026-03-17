"""
Faker integration for fraq - realistic data in fractal structures.

Allows generating real-world data (names, addresses, PESEL, NIP) 
using Faker within fraq's fractal generation.

Example:
    from fraq import generate
    from fraq.providers.faker_provider import FakerProvider
    
    records = generate({
        'name': 'faker:pl_PL.name',      # Polish names
        'nip': 'faker:pl_PL.nip',         # Polish NIP
        'temperature': 'float:10-40',      # Native fraq
    }, count=100)
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Protocol, runtime_checkable


@runtime_checkable
class ValueProvider(Protocol):
    """Protocol for value providers."""
    
    def supports(self, type_spec: str) -> bool:
        """Check if this provider supports the given type specification."""
        ...
    
    def generate(self, type_spec: str, seed: Optional[int] = None) -> Any:
        """Generate a value for the given type specification."""
        ...


class FakerProvider:
    """Faker-based value provider for realistic data generation."""
    
    def __init__(self, locale: str = "en_US"):
        self.locale = locale
        self._faker: Any = None
        self._cache: Dict[str, Callable] = {}
    
    def _get_faker(self) -> Any:
        """Lazy import and initialization of Faker."""
        if self._faker is None:
            try:
                from faker import Faker
                self._faker = Faker(self.locale)
            except ImportError:
                raise ImportError(
                    "Faker not installed. Install with: pip install fraq[faker]"
                )
        return self._faker
    
    def supports(self, type_spec: str) -> bool:
        """Check if type_spec is a faker specification.
        
        Format: 'faker:locale.method' or 'faker:method'
        Examples: 'faker:pl_PL.name', 'faker:email'
        """
        return type_spec.startswith("faker:")
    
    def generate(self, type_spec: str, seed: Optional[int] = None) -> Any:
        """Generate value using Faker.
        
        Args:
            type_spec: Format 'faker:locale.method' or 'faker:method'
            seed: Optional seed for reproducibility
        
        Returns:
            Generated value from Faker
        """
        if not self.supports(type_spec):
            raise ValueError(f"Unsupported type spec: {type_spec}")
        
        # Parse specification
        # Format: faker:locale.method or faker:method
        spec = type_spec[6:]  # Remove 'faker:' prefix
        
        if "." in spec:
            locale, method = spec.rsplit(".", 1)
            # Create locale-specific faker if needed
            if locale != self.locale:
                from faker import Faker
                faker = Faker(locale)
            else:
                faker = self._get_faker()
        else:
            method = spec
            faker = self._get_faker()
        
        # Set seed if provided for reproducibility
        if seed is not None:
            faker.seed_instance(seed)
        
        # Get method and generate
        if hasattr(faker, method):
            return getattr(faker, method)()
        
        raise ValueError(f"Unknown Faker method: {method}")


class ProviderRegistry:
    """Registry of value providers."""
    
    def __init__(self):
        self._providers: list[ValueProvider] = []
        self._faker_provider: Optional[FakerProvider] = None
    
    def register(self, provider: ValueProvider) -> None:
        """Register a value provider."""
        self._providers.append(provider)
    
    def get_faker_provider(self, locale: str = "en_US") -> FakerProvider:
        """Get or create Faker provider."""
        if self._faker_provider is None or self._faker_provider.locale != locale:
            self._faker_provider = FakerProvider(locale)
        return self._faker_provider
    
    def find_provider(self, type_spec: str) -> Optional[ValueProvider]:
        """Find provider that supports the given type specification."""
        for provider in self._providers:
            if provider.supports(type_spec):
                return provider
        
        # Check if it's a faker spec
        if type_spec.startswith("faker:"):
            return self.get_faker_provider()
        
        return None
    
    def generate(self, type_spec: str, seed: Optional[int] = None) -> Any:
        """Generate value using appropriate provider."""
        provider = self.find_provider(type_spec)
        if provider:
            return provider.generate(type_spec, seed)
        raise ValueError(f"No provider found for: {type_spec}")


# Global registry instance
_default_registry: Optional[ProviderRegistry] = None


def get_provider_registry() -> ProviderRegistry:
    """Get global provider registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = ProviderRegistry()
    return _default_registry


def generate_with_faker(type_spec: str, seed: Optional[int] = None) -> Any:
    """Convenience function to generate value with Faker.
    
    Args:
        type_spec: Format 'faker:locale.method' or 'faker:method'
                  Examples: 'faker:pl_PL.name', 'faker:email', 'faker:address'
        seed: Optional seed for reproducibility
    
    Returns:
        Generated value
    
    Raises:
        ImportError: If Faker is not installed
        ValueError: If type_spec format is invalid
    
    Examples:
        >>> generate_with_faker('faker:name')
        'John Smith'
        >>> generate_with_faker('faker:pl_PL.name')
        'Jan Kowalski'
        >>> generate_with_faker('faker:email')
        'john.smith@example.com'
    """
    registry = get_provider_registry()
    return registry.generate(type_spec, seed)
