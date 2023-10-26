from datetime import datetime
import socket
from confluent_kafka import Producer
from concurrent.futures import ThreadPoolExecutor

from loaders.bus_loader import BusDataLoader
from loaders.taxi_loader import TaxiDataLoader
from senders.sender import DataSender

KAFKA_CONFIG = {
    'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
    'client.id': socket.gethostname()
    }

def test_performance():

    batch_size = 25_000

    kafka_producer = Producer(KAFKA_CONFIG)
    bus_loader = BusDataLoader(file_index=0, start=1, end=1_000_000, batch_size=batch_size)
    
    bus_sender = DataSender(loader=bus_loader, producer=kafka_producer, topic="bus-data")

    bus_sender.send_all_data()


def main():

    test_performance()
   

if __name__ == "__main__":
    main()
