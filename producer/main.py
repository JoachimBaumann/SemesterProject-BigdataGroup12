import csv
import datetime
import time
from confluent_kafka import Producer
import socket
from dataclasses import asdict, dataclass, field
from dateutil.parser import parse as dateParse
from typing import Iterable, Iterator, List, Generator, Optional, Tuple, TypeVar
import os
import json
from collections import deque
from itertools import islice
from queue import PriorityQueue

def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Type not serializable: {type(obj)}")


T = TypeVar('T')

def window(iterable: Iterable[T], size: int = 2) -> Generator[Tuple[T, ...], None, None]:
    """Generates a sliding window over the iterable."""
    it = iter(iterable)
    win = deque(islice(it, size), maxlen=size)
    yield tuple(win)
    for item in it:
        win.append(item)
        yield tuple(win)

@dataclass
class BusData:
    RecordedAtTime: datetime.datetime = field(compare=True)
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
                RecordedAtTime=dateParse(row[0]),
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
    
    def to_json(self):
        return json.dumps(asdict(self), default=datetime_serializer)

    def __lt__(self, other):    
        return self.RecordedAtTime < other.RecordedAtTime
      
class KafkaProducerSingleton:

    KAFKA_CONFIG = {
        'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
        'client.id': socket.gethostname()
    }

    _singleton_instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super(KafkaProducerSingleton, cls).__new__(cls, *args, **kwargs)
            # Initializing the producer instance here to ensure it's done once.
            cls._singleton_instance.producer_instance = Producer(cls.KAFKA_CONFIG)
        return cls._singleton_instance

    # Send a message to Kafka.
    def send(self, topic_name: str, data: BusData):
        self.producer_instance.produce(topic_name, key=data.VehicleRef, value=data.to_json())
        self.producer_instance.flush()

    # Send a batch of messages to kafka
    def send_batch(self, topic_name: str, batch: List[BusData]):
        for data in batch:
            self.producer_instance.produce(topic_name, key=data.VehicleRef, value=data.to_json())
        self.producer_instance.flush()


class BusDataLoader:

    BASE_PATH = "datasets/bus_dataset/"
    FILENAMES = ["mta_1706.csv", "mta_1708.csv", "mta_1710.csv", "mta_1712.csv"]

    def __init__(self, file_index: int, start: int = 1, end: int | None = None, batch_size = 10_000):
        self.file_index = file_index
        self.start = start
        self.end = end
        self.batch_size = batch_size

    def construct_filepath(self, index: int) -> str:
        return os.path.join(self.BASE_PATH, self.FILENAMES[index])

    def get_busdata(self) -> Iterator[BusData]:
            """Yield BusData objects from a CSV file."""
            file_path = self.construct_filepath(self.file_index)
            
            with open(file_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                rows_to_yield = islice(csv_reader, self.start, self.end + 1 if self.end is not None else None)
                
                for row in rows_to_yield:
                    bus_data = BusData.from_row(row)
                    if bus_data:
                        yield bus_data

    def get_busdata_in_batches(self) -> Iterator[List[BusData]]:
        """Used to not read the entire dataset at once, but in batches"""
        batch: List[BusData] = []
        
        for bus_entry in self.get_busdata():
            batch.append(bus_entry)

            if len(batch) == self.batch_size:
                yield batch
                batch = []

        # Yield any remaining rows in the last batch
        if batch:
            yield batch


    def get_busdata_sorted(self) -> Iterator[BusData]:
        """Used to load data into a priority queue and yield sorted items based on RecordedAtTime."""
        priority_queue = PriorityQueue(self.batch_size)
        data_source = self.get_busdata()

        # Fill up the priority queue initially with sorted data
        for entry in islice(data_source, self.batch_size):
            priority_queue.put(entry)

        # Return the lowest priotiry, then update 
        while not priority_queue.empty():
            yield priority_queue.get()

            next_bus_entry = next(data_source, None)
            if next_bus_entry:
                priority_queue.put(next_bus_entry)


    def send_to_kafka(self):
        """Send data from the CSV to Kafka."""  
        kafka_producer = KafkaProducerSingleton()

        for batch in self.get_busdata_in_batches():
            kafka_producer.send_batch("bus", batch)

    def simulate_realtime_send(self):
        """Simulate real-time data sending based on RecordedAtTime."""
        kafka_producer = KafkaProducerSingleton()

        for previous, current in window(self.get_busdata_sorted()):
            duration = current.RecordedAtTime - previous.RecordedAtTime
            sleep_duration = duration.total_seconds()

            if sleep_duration < 0.0:
                print("Failed to send, item was not in order")
                continue

            if sleep_duration > 2.0:
                print("sleeping for", sleep_duration, "seconds...")

            time.sleep(sleep_duration)
            kafka_producer.send("bus", current)


def main():
    bus_data_loader = BusDataLoader(file_index=0, start=1, end=100_000, batch_size=10_000)

    print("Sending data to kafka")
    bus_data_loader.simulate_realtime_send()
    print("Completed task")

if __name__ == "__main__":
    main()