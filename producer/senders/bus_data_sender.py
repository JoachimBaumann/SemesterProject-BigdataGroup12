import time
from typing import List

from models.bus_data import BusData
from loaders.bus_data_loader import BusDataLoader
from utils.window import sliding_window

class BusDataSender:

    def __init__(self, loader: BusDataLoader, producer, topic: str) -> None:
        self.loader = loader
        self.producer = producer
        self.topic = topic

    def _send(self, data: BusData):
        """Send a single entry to kafka"""
        self.producer.produce(self.topic, key=data.VehicleRef, value=data.to_json())
        self.producer.flush()

    def _send_batch(self, batch: List[BusData]):
        """Send a batch of bus_data entries to kafka"""
        for data in batch:
            self.producer.produce(self.topic, key=data.VehicleRef, value=data.to_json())
        self.producer.flush()

    def send_all_data(self):
        """Send data from the CSV to Kafka."""  
        for batch in self.loader.get_busdata_batches():
            self._send_batch(batch)

    def simulate_realtime_send(self):
        """Simulate real-time data sending based on RecordedAtTime."""

        for previous, current in sliding_window(self.loader.get_busdata_entries_in_order()):
            duration = current.RecordedAtTime - previous.RecordedAtTime
            sleep_duration = duration.total_seconds()

            if sleep_duration < 0.0:
                print("Failed to send, item was not in order")
                continue

            if sleep_duration > 2.0:
                print("sleeping for", sleep_duration, "seconds...")

            self._send(current)
            time.sleep(sleep_duration)