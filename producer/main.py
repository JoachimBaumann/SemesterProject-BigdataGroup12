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

def main():

    kafka_producer = Producer(KAFKA_CONFIG)

    start_date = datetime(2019, 1, 3, 12)
    end_date = datetime(2019, 1, 3, 13)
    batch_size = 1000

    taxi_loader = TaxiDataLoader(start_date, end_date, batch_size)
    bus_loader = BusDataLoader(file_index=0, start=1, end=10000, batch_size=batch_size)
    
    taxi_sender = DataSender(loader=taxi_loader, producer=kafka_producer, topic="taxi-data")
    bus_sender = DataSender(loader=bus_loader, producer=kafka_producer, topic="bus-data")

    print("Sending data in bulk to kafka")
    taxi_sender.send_all_data()
    bus_sender.send_all_data()
    
    print("Sending Realtime data to kafka")
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(taxi_sender.simulate_realtime_send)
        executor.submit(bus_sender.simulate_realtime_send)


if __name__ == "__main__":
    main()
