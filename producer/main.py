'''
from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093',
        'client.id': socket.gethostname()}

producer = Producer(conf)

producer.produce("twitch-chat", key="val", value="From python 2.0")
producer.flush()
'''

import csv
from dataclasses import dataclass
from typing import List, Tuple, Generator, Optional

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

DATASET_PATH = "datasets/bus_dataset/"
FILE_NAME = "mta_1706.csv"
NUM_ROWS_TO_READ = 1_000_000

def read_csv(file_name: str) -> Generator[Tuple[int, List[str]], None, None]:
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        yield from enumerate(reader)


def main():
    data: List[BusData] = []
    rows = read_csv(DATASET_PATH + FILE_NAME)

    # Skip header
    next(rows)

    for index, row in rows:
        bus_data = BusData.from_row(row)
        if bus_data is not None:
            data.append(bus_data)
        if index == NUM_ROWS_TO_READ:
            print("Endig early after ", NUM_ROWS_TO_READ, " Lines")
            break


if __name__ == "__main__":
    main()