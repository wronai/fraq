"""Tests for fraq.generators."""

import pytest
from fraq.core import FraqNode
from fraq.generators import (
    HashGenerator,
    FibonacciGenerator,
    PerlinGenerator,
    SensorStreamGenerator,
)


class TestHashGenerator:
    def test_output_in_default_range(self):
        gen = HashGenerator()
        node = FraqNode(position=(1.0, 2.0, 3.0), seed=42)
        val = gen(node)
        assert 0.0 <= val < 1.0

    def test_custom_range(self):
        gen = HashGenerator(range_min=-10.0, range_max=10.0)
        node = FraqNode(position=(0.5, 0.5), seed=7)
        val = gen(node)
        assert -10.0 <= val < 10.0

    def test_deterministic(self):
        gen = HashGenerator(salt="test")
        n1 = FraqNode(position=(1.0, 2.0), seed=99)
        n2 = FraqNode(position=(1.0, 2.0), seed=99)
        assert gen(n1) == gen(n2)

    def test_different_salt_different_value(self):
        g1 = HashGenerator(salt="a")
        g2 = HashGenerator(salt="b")
        node = FraqNode(position=(1.0,), seed=0)
        assert g1(node) != g2(node)


class TestFibonacciGenerator:
    def test_depth_zero(self):
        gen = FibonacciGenerator()
        node = FraqNode(position=(0.0,), depth=0)
        assert gen(node) == 0.0  # fib(0) = 0

    def test_depth_one(self):
        gen = FibonacciGenerator()
        node = FraqNode(position=(0.0,), depth=1)
        val = gen(node)
        assert val == pytest.approx(1 / (2**31 - 1))

    def test_monotonic_for_small_depths(self):
        gen = FibonacciGenerator()
        vals = []
        for d in range(10):
            node = FraqNode(position=(0.0,), depth=d)
            vals.append(gen(node))
        # Fibonacci grows, so values should increase for small depths
        for i in range(2, 10):
            assert vals[i] >= vals[i - 1]

    def test_offset(self):
        gen = FibonacciGenerator(offset=5)
        node = FraqNode(position=(0.0,), depth=0)
        val = gen(node)
        assert val > 0  # fib(5) = 5


class TestPerlinGenerator:
    def test_output_bounded(self):
        gen = PerlinGenerator(amplitude=1.0)
        for i in range(50):
            node = FraqNode(position=(i * 0.1,), depth=i)
            val = gen(node)
            assert -2.0 <= val <= 2.0  # generous bound

    def test_smooth_variation(self):
        gen = PerlinGenerator(frequency=1.0)
        vals = []
        for i in range(20):
            node = FraqNode(position=(i * 0.05,))
            vals.append(gen(node))
        # Adjacent values should not jump wildly
        for i in range(1, len(vals)):
            assert abs(vals[i] - vals[i - 1]) < 1.0

    def test_frequency_affects_output(self):
        g1 = PerlinGenerator(frequency=1.0)
        g2 = PerlinGenerator(frequency=10.0)
        node = FraqNode(position=(1.0,))
        assert g1(node) != g2(node)


class TestSensorStreamGenerator:
    def test_returns_dict(self):
        gen = SensorStreamGenerator()
        node = FraqNode(position=(0.0, 0.0, 0.0))
        data = gen(node)
        assert isinstance(data, dict)
        assert "temperature" in data
        assert "humidity" in data
        assert "pressure" in data
        assert "depth" in data

    def test_custom_base_values(self):
        gen = SensorStreamGenerator(base_temp=100.0)
        node = FraqNode(position=(0.0,), seed=0)
        data = gen(node)
        # Should be near 100 ± noise
        assert 90.0 <= data["temperature"] <= 110.0

    def test_deterministic(self):
        gen = SensorStreamGenerator()
        n1 = FraqNode(position=(1.0, 2.0), seed=42)
        n2 = FraqNode(position=(1.0, 2.0), seed=42)
        assert gen(n1) == gen(n2)

    def test_different_positions_different_data(self):
        gen = SensorStreamGenerator()
        n1 = FraqNode(position=(0.0, 0.0))
        n2 = FraqNode(position=(5.0, 5.0))
        # Very likely different (not guaranteed but astronomically unlikely)
        assert gen(n1) != gen(n2)
