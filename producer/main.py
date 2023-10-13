from datetime import datetime
import socket
from confluent_kafka import Producer

from loaders.bus_loader import BusDataLoader
from loaders.taxi_loader import TaxiDataLoader
from senders.sender import DataSender

KAFKA_TOPIC = "bus-data"
KAFKA_CONFIG = {
    'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
    'client.id': socket.gethostname()
}
         
def main():

    kafka_producer = Producer(KAFKA_CONFIG)

    start_date = datetime(2019, 3, 1, 12, 20)
    end_date = datetime(2019, 3, 1, 12, 30)
    batch_size = 1000

    taxi_loader = TaxiDataLoader(start_date, end_date, batch_size)
    bus_loader = BusDataLoader(file_index=0, start=1, end=100, batch_size= batch_size)
    
    sender = DataSender(loader=taxi_loader, producer=kafka_producer, topic=KAFKA_TOPIC)

    print("Sending Bulk data to kafka")
    sender.send_all_data()
    print("Completed")

    print("Simulating realtime sending of data to kafka")
    sender.simulate_realtime_send()
    print("Completed")

if __name__ == "__main__":
    main()