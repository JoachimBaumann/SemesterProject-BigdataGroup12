from datetime import datetime
from typing import Iterator, List, Optional, Tuple
from itertools import islice
import os
import sqlite3
from dateutil.parser import parse as date_parse
from models.taxi_data import TaxiData
from loaders.interface import DataLoader

class TaxiDataLoader(DataLoader[TaxiData]):

    def __init__(self, start_date: datetime, end_date: datetime, batch_size=10_000, base_path: str="datasets/taxi_dataset/2019/"):
        assert start_date.month == end_date.month, "Date range must be within the same month"
        self.date_from = start_date
        self.date_to = end_date
        self.batch_size = batch_size
        self.base_path = base_path 
        self.filepath = self._construct_filepath()

    def _construct_filepath(self) -> str:
        """Construct the path based on the month."""
        month = self.date_from.month
        filename = f"2019-{month:02}.sqlite"
        return os.path.join(self.base_path, filename)

    def _connect_to_database(self) -> Optional[sqlite3.Connection]:
        try:
            # Directly open a new connection for the thread
            return sqlite3.connect(self.filepath)
        except sqlite3.Error as e:
            print(f"Error when connecting to the database: {e}")
            return None

    def _execute_query(self, conn: sqlite3.Connection, query: str) -> Iterator[Tuple]:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(query)
                while (batch := cursor.fetchmany(self.batch_size)):
                    for row in batch:
                        yield row
        except sqlite3.Error as e:
            print(f"SQLite error when executing query: {e}")
        finally:
            cursor.close()
            conn.close()  # Close the connection

    def _get_raw_entries(self) -> Iterator[Tuple]:
        """Yield rows from the SQLite file in a sorted manner."""
        
        # Construct the query using date_from and date_to
        query = f"SELECT * FROM tripdata WHERE tpep_pickup_datetime BETWEEN '{self.date_from}' AND '{self.date_to}' ORDER BY tpep_pickup_datetime ASC;"
        
        conn = self._connect_to_database()
        if conn:
            yield from self._execute_query(conn, query)

    def get_entries_in_order(self) -> Iterator[TaxiData]:
        """Yield TaxiData objects from the SQLite file."""
        for row in self._get_raw_entries():
            taxi_data = self._from_raw(row)
            if taxi_data:
                yield taxi_data

    def get_batches(self) -> Iterator[List[TaxiData]]:
        """ 
        Divides the dataset into batches of length `batch_size`. 
        The last batch may be smaller if the total entries aren't a multiple of `batch_size`. 
        """
        iterable = iter(self.get_entries_in_order())
        while batch := list(islice(iterable, self.batch_size)):
            yield batch

    def _from_raw(self, row) -> Optional[TaxiData]:
        '''Convert a row into a TaxiData object.'''
        try:
            return TaxiData(
                vendorid=int(row[0]),
                tpep_pickup_datetime=date_parse(row[1]),
                tpep_dropoff_datetime=date_parse(row[2]),
                passenger_count=int(row[3]),
                trip_distance=float(row[4]),
                ratecodeid=int(row[5]),
                store_and_fwd_flag=bool(row[6]),
                pulocationid=int(row[7]),
                dolocationid=int(row[8]),
                payment_type=int(row[9]),
                fare_amount=float(row[10]),
                extra=float(row[11]),
                mta_tax=float(row[12]),
                tip_amount=float(row[13]),
                tolls_amount=float(row[14]),
                improvement_surcharge=float(row[15]),
                total_amount=float(row[16]),
                congestion_surcharge=row[17]
            )
        except (ValueError, IndexError):
            return None
