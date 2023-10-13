import socket
from confluent_kafka import Producer

from loaders.bus_data_loader import BusDataLoader
from senders.bus_data_sender import BusDataSender

KAFKA_TOPIC = "bus-data"
KAFKA_CONFIG = {
    'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
    'client.id': socket.gethostname()
}
         
def main():

    kafka_producer = Producer(KAFKA_CONFIG)

    loader = BusDataLoader(file_index=0, start=1, end=100, batch_size=10_000)
    sender = BusDataSender(loader=loader, producer=kafka_producer, topic=KAFKA_TOPIC)

    print("Sending Bulk data to kafka")
    sender.send_all_data()
    print("Completed")

    print("Simulating realtime sending of data to kafka")
    sender.simulate_realtime_send()
    print("Completed")

if __name__ == "__main__":
    main()