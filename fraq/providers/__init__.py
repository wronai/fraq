"""
Value providers for fraq - integration with external data libraries.

This package provides bridges to popular data generation libraries:
- Faker: Realistic names, addresses, PESEL, NIP, etc.
- (Future) Mimesis: Alternative to Faker
- (Future) SDV: Synthetic data for ML

Example:
    from fraq import generate
    
    records = generate({
        'name': 'faker:name',           # Realistic names
        'email': 'faker:email',          # Realistic emails
        'temperature': 'float:10-40',  # Native fraq
    }, count=100)
"""

from __future__ import annotations

from fraq.providers.faker_provider import (
    FakerProvider,
    ProviderRegistry,
    ValueProvider,
    generate_with_faker,
    get_provider_registry,
)

__all__ = [
    "FakerProvider",
    "ProviderRegistry",
    "ValueProvider",
    "generate_with_faker",
    "get_provider_registry",
]
