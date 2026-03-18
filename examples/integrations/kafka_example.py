"""
Apache Kafka integration example for fraq.

Produces fractal data to Kafka topics.
"""

from __future__ import annotations

import json
import time

from kafka import KafkaProducer, KafkaConsumer

from fraq import generate, stream


KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC_DATA = "fraq-data"
TOPIC_STREAM = "fraq-stream"


def produce_to_kafka(count: int = 1000) -> None:
    """Generate fraq data and produce to Kafka."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    fields = {
        'temperature': 'float:10-40',
        'humidity': 'float:30-80',
        'sensor_id': 'str',
        'timestamp': 'str',
    }
    
    print(f"Producing {count} records to topic: {TOPIC_DATA}")
    
    for i, record in enumerate(generate(fields, count=count, seed=42)):
        record['_index'] = i
        producer.send(TOPIC_DATA, record)
        
        if (i + 1) % 100 == 0:
            print(f"  Produced: {i + 1}/{count}")
    
    producer.flush()
    print("Production complete")


def stream_to_kafka(duration_seconds: int = 30) -> None:
    """Stream fraq data to Kafka for specified duration."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print(f"Streaming to {TOPIC_STREAM} for {duration_seconds}s...")
    
    start_time = time.time()
    count = 0
    
    for record in stream(
        {'value': 'float:0-100'},
        count=None,  # Infinite
        interval=0.1
    ):
        record['_timestamp'] = time.time()
        producer.send(TOPIC_STREAM, record)
        count += 1
        
        if time.time() - start_time >= duration_seconds:
            break
        
        if count % 100 == 0:
            print(f"  Streamed: {count} records")
    
    producer.flush()
    print(f"Streamed {count} records in {duration_seconds}s")


def consume_from_kafka(topic: str = TOPIC_DATA, max_records: int = 10) -> None:
    """Consume and display fraq data from Kafka."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        consumer_group_id='fraq-consumer'
    )
    
    print(f"Consuming from {topic} (max {max_records} records):")
    
    for i, message in enumerate(consumer):
        print(f"  {i+1}: {message.value}")
        
        if i + 1 >= max_records:
            break
    
    consumer.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python kafka_example.py [produce|stream|consume]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "produce":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        produce_to_kafka(count)
    elif command == "stream":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        stream_to_kafka(duration)
    elif command == "consume":
        topic = sys.argv[2] if len(sys.argv) > 2 else TOPIC_DATA
        max_rec = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        consume_from_kafka(topic, max_rec)
    else:
        print(f"Unknown command: {command}")
