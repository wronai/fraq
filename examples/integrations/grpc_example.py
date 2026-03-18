"""
gRPC integration example for fraq.

Generates .proto file and shows how to use fraq with gRPC.
"""

from __future__ import annotations

from fraq import FraqSchema, to_proto


def generate_proto_file():
    """Generate a .proto file for fraq service."""
    schema = FraqSchema()
    schema.add_field("temperature", "float")
    schema.add_field("humidity", "float")
    schema.add_field("sensor_id", "str")
    
    proto_content = to_proto(
        schema,
        package="fraq",
        message_name="SensorReading"
    )
    
    print("Generated proto file content:")
    print("=" * 60)
    print(proto_content)
    print("=" * 60)
    
    # Save to file
    with open("fraq_service.proto", "w") as f:
        f.write(proto_content)
    
    print("\nSaved to: fraq_service.proto")
    print("\nTo compile:")
    print("  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. fraq_service.proto")


def example_grpc_server_stub():
    """Example gRPC server using fraq data."""
    code = '''
import grpc
from concurrent import futures

# Generated from proto
import fraq_service_pb2
import fraq_service_pb2_grpc

from fraq import generate


class FraqServicer(fraq_service_pb2_grpc.FraqServiceServicer):
    def Zoom(self, request, context):
        # Generate fraq data
        records = generate({
            'temperature': 'float:0-100',
            'humidity': 'float:0-100',
        }, count=request.limit)
        
        # Convert to proto messages
        proto_records = [
            fraq_service_pb2.SensorReading(
                temperature=r['temperature'],
                humidity=r['humidity'],
                sensor_id=r.get('sensor_id', 'unknown')
            )
            for r in records
        ]
        
        return fraq_service_pb2.ZoomResponse(
            records=proto_records,
            total=len(proto_records)
        )
    
    def Stream(self, request, context):
        from fraq import stream
        
        for record in stream({'value': 'float'}, count=request.count):
            yield fraq_service_pb2.SensorReading(
                temperature=record['value'],
                humidity=record['value'] * 0.8,
                sensor_id='stream'
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraq_service_pb2_grpc.add_FraqServiceServicer_to_server(
        FraqServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
'''
    print("\nExample gRPC server code:")
    print(code)


if __name__ == "__main__":
    generate_proto_file()
    example_grpc_server_stub()
