import csv
import datetime
import time
from confluent_kafka import Producer
import socket
from dataclasses import asdict, dataclass
from itertools import islice
from dateutil.parser import parse as dateParse
from typing import List, Tuple, Generator, Optional, Callable
import os
import json

@dataclass
class BusData:
    RecordedAtTime: str
    DirectionRef: int
    PublishedLineName: str
    OriginName: str
    OriginLat: float
    OriginLong: float
    DestinationName: str 
    DestinationLat: float
    DestinationLong: float
    VehicleRef: str
    VehicleLocationLatitude: float
    VehicleLocationLongitude: float 
    NextStopPointName: str
    ArrivalProximityText: str
    DistanceFromStop: int 
    ExpectedArrivalTime: str
    ScheduledArrivalTime: str

    @classmethod
    def from_row(cls, row: List[str]) -> Optional['BusData']:
        try:
            return cls(
                RecordedAtTime=row[0],
                DirectionRef=int(row[1]),
                PublishedLineName=row[2],
                OriginName=row[3],
                OriginLat=float(row[4]),
                OriginLong=float(row[5]),
                DestinationName=row[6],
                DestinationLat=float(row[7]),
                DestinationLong=float(row[8]),
                VehicleRef=row[9],
                VehicleLocationLatitude=float(row[10]),
                VehicleLocationLongitude=float(row[11]),
                NextStopPointName=row[12],
                ArrivalProximityText=row[13],
                DistanceFromStop=int(row[14]),
                ExpectedArrivalTime=row[15],
                ScheduledArrivalTime=row[16]
            )
        except (ValueError, IndexError):
            return None
      
class KafkaProducerSingleton:

    KAFKA_CONFIG = {
        'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
        'client.id': socket.gethostname()
    }

    _singleton_instance = None
    
    # Ensure only one instance of the class can be created.
    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super(KafkaProducerSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._singleton_instance

    # Initialize Kafka producer.
    def __init__(self):
        # Ensure producer is initialized once.
        if not hasattr(self, 'producer_instance'):
            self.producer_instance = Producer(self.KAFKA_CONFIG)

    # Send a message to Kafka.
    def send(self, topic_name: str, key_value: str, message_value: str):
        self.producer_instance.produce(topic_name, key=key_value, value=message_value)
        self.producer_instance.flush()


class BusDataLoader:

    BASE_PATH = "datasets/bus_dataset/"
    FILENAMES = ["mta_1706.csv", "mta_1708.csv", "mta_1710.csv", "mta_1712.csv"]

    # Initialize loader and set up the CSV reader generator.
    def __init__(self, file_index: int, start: int = 0, end: int = None):
        self.loaded_data: List[BusData] = []
        file_path = self._construct_filepath(file_index)
        self.csv_row_generator = self._generate_csv_rows(file_path, start, end)

    # Return full path of the desired CSV file.
    def _construct_filepath(self, index: int) -> str:
        return os.path.join(self.BASE_PATH, self.FILENAMES[index])

    # Yield rows from the specified CSV file.
    def _generate_csv_rows(self, file_path: str, start_index: int, end_index: int) -> Generator[List[str], None, None]:
        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            rows_to_yield = islice(csv_reader, start_index, end_index + 1 if end_index is not None else None)
            for row in rows_to_yield:
                yield row

    # Load data from the CSV into memory.
    def load_from_csv(self):
        for row in self.csv_row_generator:
            bus_entry = BusData.from_row(row)
            if bus_entry:
                self.loaded_data.append(bus_entry)

    # Send data from the CSV to Kafka.
    def send_to_kafka(self):
        kafka_producer = KafkaProducerSingleton()

        for row in self.csv_row_generator:
            bus_entry = BusData.from_row(row)
            if bus_entry:
                json_string = json.dumps(asdict(bus_entry))
                kafka_producer.send("bus", bus_entry.VehicleRef, json_string)

    def simulate_realtime_send(self):
        """Simulate real-time data sending based on RecordedAtTime."""
        kafka_producer = KafkaProducerSingleton()
        
        prev_time = None

        for row in self.csv_row_generator:
            bus_entry = BusData.from_row(row)
            if bus_entry:

                current_time = dateParse(bus_entry.RecordedAtTime)

            if prev_time:
                sleep_duration = (current_time - prev_time).total_seconds()
                time.sleep(sleep_duration)

                json_string = json.dumps(asdict(bus_entry))
                kafka_producer.send("bus", bus_entry.VehicleRef, json_string)
                prev_time = current_time


def main():
    bus_data_loader = BusDataLoader(file_index=0, start=1, end=10)

    print("Sending data to kafka")
    bus_data_loader.simulate_realtime_send()
    print("Completed task")

if __name__ == "__main__":
    main()