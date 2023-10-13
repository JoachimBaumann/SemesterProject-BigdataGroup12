import time
from typing import List
from loaders.interface import DataLoader
from models.interfaces import Data
from utils.window import sliding_window

class DataSender:

    def __init__(self, loader: DataLoader[Data], producer, topic: str) -> None:
        self.loader = loader
        self.producer = producer
        self.topic = topic

    def _send(self, data: Data):
        """Send a single entry to kafka"""
        self.producer.produce(self.topic, key=data.unique_identifier, value=data.to_json())
        self.producer.flush()

    def _send_batch(self, batch: List[Data]):
        """Send a batch of data entries to kafka"""
        for data in batch:
            self.producer.produce(self.topic, key=data.unique_identifier, value=data.to_json())
        self.producer.flush()

    def send_all_data(self):
        """Send data from the loader to Kafka."""
        for batch in self.loader.get_batches():
            self._send_batch(batch)

    def simulate_realtime_send(self):
        """Simulate real-time data sending based on a timestamp attribute."""
        for previous, current in sliding_window(self.loader.get_entries_in_order()):
            duration = current.timestamp - previous.timestamp
            sleep_duration = duration.total_seconds()

            if sleep_duration < 0.0:
                print("Failed to send, item was not in order")
                continue

            if sleep_duration > 2.0:
                print("sleeping for", sleep_duration, "seconds...")

            self._send(current)
            time.sleep(sleep_duration)
