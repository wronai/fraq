#!/usr/bin/env python3
"""IoT examples - UPROSZCZONE używając text2fraq."""

from __future__ import annotations

from fraq.text2fraq import text2fraq


def example_1_sensors():
    """Generuj sensory - UPROSZCZONE."""
    print("=" * 60)
    print("1. SENSORY (text2fraq)")
    print("=" * 60)

    # Uproszczone: jedna linia zamiast schema + transformacje
    result = text2fraq("generuj 3 sensory temperatura wilgotność ciśnienie 5 odczytów")
    print(f"Wynik: {len(result) if isinstance(result, list) else 'N/A'} rekordów")


def example_2_mqtt():
    """Generuj MQTT - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. MQTT PAYLOADS (text2fraq)")
    print("=" * 60)

    result = text2fraq("generuj 5 payloadów mqtt topics factory/sensors json")
    print(f"Generated {len(result) if isinstance(result, list) else 'N/A'} MQTT messages")


def example_3_health():
    """Health monitoring - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. DEVICE HEALTH (text2fraq)")
    print("=" * 60)

    result = text2fraq("monitoruj health 20 urządzeń battery signal status")
    print(f"Devices: {len(result) if isinstance(result, list) else 'N/A'}")


if __name__ == "__main__":
    example_1_sensors()
    example_2_mqtt()
    example_3_health()
    print("\n" + "=" * 60)
    print("Done! Uproszczone wersje z text2fraq")
    print("=" * 60)
