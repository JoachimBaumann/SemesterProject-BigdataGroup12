from datetime import datetime, timedelta
import socket
from confluent_kafka import Producer

from loaders.mocked_bus_loader import MockedBusDataLoader
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


def main():

    test_performance()
   

if __name__ == "__main__":
    main()
