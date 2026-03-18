"""Tests for Faker provider integration."""

import pytest
from fraq.providers import FakerProvider, ProviderRegistry, generate_with_faker


class TestFakerProvider:
    """Test Faker provider."""
    
    def test_supports_faker_spec(self):
        """Test that provider supports faker specifications."""
        provider = FakerProvider()
        assert provider.supports("faker:name")
        assert provider.supports("faker:pl_PL.name")
        assert provider.supports("faker:email")
    
    def test_does_not_support_non_faker(self):
        """Test that provider rejects non-faker specs."""
        provider = FakerProvider()
        assert not provider.supports("float:10-40")
        assert not provider.supports("str")
        assert not provider.supports("int")
    
    def test_generate_raises_without_faker(self):
        """Test that generate raises ImportError without Faker installed."""
        provider = FakerProvider()
        try:
            result = provider.generate("faker:name")
            # If Faker is installed, should return a string
            assert isinstance(result, str)
        except ImportError:
            # Expected if Faker not installed
            pass


class TestProviderRegistry:
    """Test provider registry."""
    
    def test_register_provider(self):
        """Test registering custom provider."""
        registry = ProviderRegistry()
        
        class MockProvider:
            def supports(self, spec):
                return spec == "mock:test"
            def generate(self, spec, seed=None):
                return "mock_value"
        
        registry.register(MockProvider())
        provider = registry.find_provider("mock:test")
        assert provider is not None
    
    def test_find_faker_provider(self):
        """Test finding Faker provider."""
        registry = ProviderRegistry()
        provider = registry.find_provider("faker:name")
        assert provider is not None
        assert isinstance(provider, FakerProvider)


class TestGenerateWithFaker:
    """Test generate_with_faker convenience function."""
    
    def test_function_exists(self):
        """Test that function exists and is callable."""
        assert callable(generate_with_faker)
    
    def test_invalid_spec_raises(self):
        """Test that invalid spec raises error."""
        with pytest.raises((ValueError, ImportError)):
            generate_with_faker("invalid:spec")
