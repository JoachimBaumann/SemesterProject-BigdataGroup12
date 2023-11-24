from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import socket

from dataclasses import asdict

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from models.interfaces import Data

from loaders.mocked_bus_loader import MockedBusDataLoader
from loaders.bus_loader import BusDataLoader
from loaders.taxi_loader import TaxiDataLoader
from senders.sender import DataSender



KAFKA_CONFIG = {
    'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
    'client.id': socket.gethostname()
    }

SCHEMA_CONFIG = {
    'url': 'http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081'
}

def test_performance():

    kafka_producer = Producer(KAFKA_CONFIG)
    mock_loader = MockedBusDataLoader(file_index=0, duration=timedelta(seconds=30), batch_size=1_000)
    
    bus_sender = DataSender(loader=mock_loader, producer=kafka_producer, topic="bus-data")
    bus_sender.send_all_data()

def test_realtime():
    producer = Producer(KAFKA_CONFIG)
    schema_client = SchemaRegistryClient(SCHEMA_CONFIG)

    bus_loader = BusDataLoader(file_index=1, start=1, end=100_000, batch_size=25_000)
    taxi_loader = TaxiDataLoader(datetime(2019, 1, 1), datetime(2019, 1, 30))

    bus_sender = DataSender(loader=bus_loader, producer=producer, schema_client=schema_client, topic="bus-data")
    taxi_sender = DataSender(loader=taxi_loader, producer=producer, schema_client=schema_client, topic="taxi-data")
    

    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Schedule the sending functions to be executed
        executor.submit(bus_sender.simulate_realtime_send)
        executor.submit(taxi_sender.simulate_realtime_send)


def to_dict(busdata: Data, ctx):
    
    return asdict(busdata)

def main():
    test_realtime()

if __name__ == "__main__":
    main()
