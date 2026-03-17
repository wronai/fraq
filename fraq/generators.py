"""
Procedural generators for FraqNode values.

A generator is any callable ``(FraqNode) -> scalar``.  This module provides
several useful built-ins that produce deterministic, interesting data from
a node's position and seed.
"""

from __future__ import annotations

import hashlib
import math
import struct
from typing import Any

from fraq.core import FraqNode, _vec_hash


class HashGenerator:
    """Deterministic pseudo-random values via SHA-256.

    Parameters
    ----------
    salt : str
        Extra entropy mixed into every hash.
    range_min, range_max : float
        Output is scaled to ``[range_min, range_max)``.
    """

    def __init__(
        self, salt: str = "", range_min: float = 0.0, range_max: float = 1.0
    ):
        self.salt = salt
        self.range_min = range_min
        self.range_max = range_max

    def __call__(self, node: FraqNode) -> float:
        raw = hashlib.sha256(f"{self.salt}:{node.seed}:{node.position}".encode()).digest()
        h = int.from_bytes(raw[:4], "big")
        t = h / (2**32)
        return self.range_min + t * (self.range_max - self.range_min)


class FibonacciGenerator:
    """Value based on generalised Fibonacci sequence at the node's depth.

    The output is ``fib(depth + offset) mod modulus``, scaled to [0, 1).
    """

    def __init__(self, offset: int = 0, modulus: int = 2**31 - 1):
        self.offset = offset
        self.modulus = modulus
        self._cache: dict[int, int] = {0: 0, 1: 1}

    def _fib(self, n: int) -> int:
        if n in self._cache:
            return self._cache[n]
        self._cache[n] = (self._fib(n - 1) + self._fib(n - 2)) % self.modulus
        return self._cache[n]

    def __call__(self, node: FraqNode) -> float:
        idx = abs(node.depth + self.offset)
        return self._fib(idx) / self.modulus


class PerlinGenerator:
    """Simplified 1-D Perlin-ish noise from the L2 norm of position.

    Useful for smooth, organic-looking sensor streams.
    """

    def __init__(self, frequency: float = 1.0, amplitude: float = 1.0):
        self.frequency = frequency
        self.amplitude = amplitude

    def __call__(self, node: FraqNode) -> float:
        t = sum(x * x for x in node.position) ** 0.5
        t *= self.frequency
        # Cheap smooth noise: sum of phase-shifted sines
        val = (
            math.sin(t * 1.0)
            + 0.5 * math.sin(t * 2.3 + 1.7)
            + 0.25 * math.sin(t * 5.1 + 3.1)
        )
        return self.amplitude * val / 1.75  # normalise roughly to [-amp, amp]


class SensorStreamGenerator:
    """Simulate an infinite IoT sensor stream.

    Produces dict payloads with ``timestamp``, ``temperature``, ``humidity``
    and ``pressure`` fields — all deterministic from the node's coordinates.
    """

    def __init__(
        self,
        base_temp: float = 22.0,
        base_humidity: float = 55.0,
        base_pressure: float = 1013.25,
    ):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        self.base_pressure = base_pressure

    def __call__(self, node: FraqNode) -> dict[str, Any]:
        h = _vec_hash(node.position, node.seed)
        t_noise = ((h % 1000) - 500) / 100.0
        h_noise = ((h >> 10) % 1000 - 500) / 50.0
        p_noise = ((h >> 20) % 1000 - 500) / 200.0
        return {
            "timestamp_offset": node.depth,
            "temperature": round(self.base_temp + t_noise, 2),
            "humidity": round(self.base_humidity + h_noise, 2),
            "pressure": round(self.base_pressure + p_noise, 2),
            "depth": node.depth,
            "position": list(node.position),
        }
