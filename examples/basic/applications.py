#!/usr/bin/env python3
"""Applications examples - UPROSZCZONE z nowym API fraq."""

from __future__ import annotations

from fraq import generate, stream, FraqSchema


def example_1_iot_sensors():
    """IoT sensors - UPROSZCZONE."""
    print("=" * 60)
    print("1. IOT SENSORS (UPROSZCZONE)")
    print("=" * 60)

    # UPROSZCZONE: generate() dla sensorów
    readings = generate({
        'device_id': 'str',
        'temperature': 'float:15-30',
        'humidity': 'float:30-80',
        'battery': 'float:20-100',
    }, count=20)

    # Group by device
    devices = {}
    for r in readings:
        did = r['device_id']
        if did not in devices:
            devices[did] = []
        devices[did].append(r)

    print(f"Data from {len(devices)} devices:")
    for did, dev_readings in list(devices.items())[:3]:
        avg_temp = sum(r['temperature'] for r in dev_readings) / len(dev_readings)
        print(f"  {did}: {len(dev_readings)} readings, avg temp={avg_temp:.1f}°C")


def example_2_erp_invoices():
    """ERP invoices - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("2. ERP INVOICES (UPROSZCZONE)")
    print("=" * 60)

    invoices = generate({
        'invoice_id': 'str',
        'amount': 'float:100-10000',
        'vat_rate': 'float:0.08-0.23',
        'client_id': 'str',
        'paid': 'bool',
    }, count=10)

    total = sum(inv['amount'] for inv in invoices)
    paid = sum(inv['amount'] for inv in invoices if inv['paid'])
    unpaid = total - paid

    print(f"Invoices: {len(invoices)}")
    print(f"  Total: ${total:,.2f}")
    print(f"  Paid: ${paid:,.2f}, Unpaid: ${unpaid:,.2f}")


def example_3_ai_training():
    """AI training data - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("3. AI TRAINING DATA (UPROSZCZONE)")
    print("=" * 60)

    # Classification dataset
    dataset = generate({
        'feature_1': 'float',
        'feature_2': 'float',
        'feature_3': 'float',
        'label': 'bool',
    }, count=1000)

    # Split
    train_size = int(0.8 * len(dataset))
    train = dataset[:train_size]
    test = dataset[train_size:]

    print(f"Dataset: {len(dataset)} samples")
    print(f"  Train: {len(train)}, Test: {len(test)}")

    # Class distribution
    positive = sum(1 for s in train if s['label'])
    print(f"  Class balance: {positive}/{len(train)-positive}")


def example_4_devops_metrics():
    """DevOps metrics - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("4. DEVOPS METRICS (UPROSZCZONE)")
    print("=" * 60)

    # Stream metrics
    print("Streaming 5 system metrics:")
    for i, metric in enumerate(stream({
        'cpu_percent': 'float:0-100',
        'memory_mb': 'int:100-16000',
        'request_id': 'str',
    }, count=5)):
        status = "ALERT" if metric['cpu_percent'] > 80 else "OK"
        print(f"  [{i}] CPU={metric['cpu_percent']:.1f}% MEM={metric['memory_mb']}MB {status}")


def example_5_finance():
    """Finance - UPROSZCZONE."""
    print("\n" + "=" * 60)
    print("5. FINANCE LEASING (UPROSZCZONE)")
    print("=" * 60)

    scenarios = generate({
        'monthly_rate': 'float:500-5000',
        'total_cost': 'float:20000-200000',
        'down_payment': 'float:0-50000',
    }, count=5)

    print("Leasing scenarios:")
    for i, s in enumerate(scenarios, 1):
        print(f"  {i}. ${s['monthly_rate']:.0f}/mo, total ${s['total_cost']:,.0f}")


if __name__ == "__main__":
    example_1_iot_sensors()
    example_2_erp_invoices()
    example_3_ai_training()
    example_4_devops_metrics()
    example_5_finance()
    print("\n" + "=" * 60)
    print("Done! Applications w wersji uproszczonej")
    print("=" * 60)
