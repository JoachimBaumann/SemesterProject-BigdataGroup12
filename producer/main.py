from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import socket
from confluent_kafka import Producer

from loaders.mocked_bus_loader import MockedBusDataLoader
from loaders.bus_loader import BusDataLoader
from loaders.taxi_loader import TaxiDataLoader
from senders.sender import DataSender

KAFKA_CONFIG = {
    'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
    'client.id': socket.gethostname()
    }

def test_performance():

    kafka_producer = Producer(KAFKA_CONFIG)
    mock_loader = MockedBusDataLoader(file_index=0, duration=timedelta(seconds=30), batch_size=1_000)
    
    bus_sender = DataSender(loader=mock_loader, producer=kafka_producer, topic="bus-data")
    bus_sender.send_all_data()

def test_realtime():
    kafka_producer = Producer(KAFKA_CONFIG)

    bus_loader = BusDataLoader(file_index=1, start=1, end=100_000, batch_size=25_000)
    taxi_loader = TaxiDataLoader(datetime(2019, 1, 1), datetime(2019, 1, 30))
    
    bus_sender = DataSender(loader=bus_loader, producer=kafka_producer, topic="bus-data")
    taxi_sender = DataSender(loader=taxi_loader, producer=kafka_producer, topic="taxi-data")

    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Schedule the sending functions to be executed
        executor.submit(bus_sender.simulate_realtime_send)
        executor.submit(taxi_sender.simulate_realtime_send)


def main():

    test_realtime()
   

if __name__ == "__main__":
    main()
