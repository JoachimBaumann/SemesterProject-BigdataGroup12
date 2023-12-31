import csv
from datetime import datetime, timedelta
import os
from itertools import islice
from queue import PriorityQueue
from typing import Iterator, List, Optional
from dateutil.parser import parse as date_parse
from models.bus_data import BusData
from loaders.interface import DataLoader


class MockedBusDataLoader(DataLoader[BusData]):

    BASE_PATH = "datasets/bus_dataset/"
    FILENAMES = ["mta_1706.csv", "mta_1708.csv", "mta_1710.csv", "mta_1712.csv"]

    def __init__(self, file_index: int, duration: timedelta, batch_size = 10_000):
        self.file_index = file_index
        self.start = 1
        self.end = batch_size
        self.duration = duration
        self.batch_size = batch_size
        
        file_path = self._construct_filepath()
  
        if not os.path.exists(file_path):
            print(f"Downloading {file_path}...")
            download_objects(prefix=file_path)


    def _construct_filepath(self) -> str:
        """Convert file index to a filepath"""
        index = self.file_index
        return os.path.join(self.BASE_PATH, self.FILENAMES[index])

    def _get_raw_rows(self) -> Iterator[List[str]]:
        """Yield rows from the CSV file as lists of strings."""
        file_path = self._construct_filepath()
        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            yield from islice(csv_reader, self.start, self.end + 1 if self.end is not None else None)

    def _get_busdata_entries(self) -> Iterator[BusData]:
        """Yield BusData objects from the CSV file."""
        for row in self._get_raw_rows():
            bus_data = self._from_row(row)
            if bus_data:
                yield bus_data

    def get_entries_in_order(self) -> Iterator[BusData]:
        """Used to load data into a priority queue and yield sorted items based on RecordedAtTime."""
        priority_queue = PriorityQueue(self.batch_size)
        data_source = self._get_busdata_entries()

        # Fill up the priority queue initially with sorted data
        for entry in islice(data_source, self.batch_size):
            priority_queue.put(entry)

        # Return the lowest priotiry, then update 
        while not priority_queue.empty():
            yield priority_queue.get()

            next_bus_entry = next(data_source, None)
            if next_bus_entry:
                priority_queue.put(next_bus_entry)

    def get_batches(self) -> Iterator[List[BusData]]:
        iterable = iter(self._get_busdata_entries())

        batch = list(islice(iterable, self.batch_size))
        start_time = datetime.now()

        while datetime.now() - start_time < self.duration:
            yield batch
    
    def get_avro_schema(self) -> str:
        return BusData.avro_schema_to_python()


    def _from_row(self, row: List[str]) -> Optional[BusData]:
        '''Convert a list of strings into busdata object'''
        try:
            timestamp = date_parse(row[0])
            timestamp = timestamp.replace(year=2019)
            return BusData(
                RecordedAtTime=timestamp,
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