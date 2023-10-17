import csv
from datetime import datetime
import os
from itertools import islice
from queue import PriorityQueue
from typing import Iterator, List, Optional
from dateutil.parser import parse as date_parse
from models.bus_data import BusData


class BusDataLoader:

    BASE_PATH = "datasets/bus_dataset/"
    FILENAMES = ["mta_1706.csv", "mta_1708.csv", "mta_1710.csv", "mta_1712.csv"]

    def __init__(self, file_index: int, start: int = 1, end: int | None = None, batch_size = 10_000):
        self.file_index = file_index
        self.start = start
        self.end = end
        self.batch_size = batch_size

    def set_range_from_datetime(self, date_start: datetime, date_end: datetime):
        best_start_tuple = 0, float('inf')
        best_end_tuple = 0, float('inf')

        print("Looking for row to start from")

        for i, row in enumerate(self._get_raw_rows()):

            timestamp = date_parse(row[0])
            
            diff_start = abs((date_start - timestamp).total_seconds())
            diff_end = abs((date_end - timestamp).total_seconds())

            if diff_start < best_start_tuple[1]:
                print(f"updateing start value: i: {i}, date: {timestamp}")
                best_start_tuple = i, diff_start
            
            if diff_end < best_end_tuple[1]:
                print(f"updateing end value: i: {i}, date: {timestamp}")
                best_end_tuple = i, diff_end
        
        self.start = best_start_tuple[0]
        self.end = best_end_tuple[0]

        print(self.start, self.end)

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
        """ Divides the dataset into batches of of length `batch_size`. The last batch may be smaller if the total entries aren't a multiple of `batch_size`. """
        iterable = iter(self._get_busdata_entries())

        while batch := list(islice(iterable, self.batch_size)):
            yield batch


    def _from_row(self, row: List[str]) -> Optional[BusData]:
        '''Convert a list of strings into busdata object'''
        try:
            return BusData(
                RecordedAtTime=date_parse(row[0]),
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