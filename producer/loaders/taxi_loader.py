from datetime import datetime
from typing import Iterator, List, Optional, Tuple
from itertools import islice
import os
import sqlite3
from dateutil.parser import parse as date_parse
from models.taxi_data import TaxiData
from loaders.interface import DataLoader

class SQLiteConnectionPool:
    def __init__(self, database_path: str, pool_size: int = 5):
        self.database_path = database_path
        self.pool_size = pool_size
        self._pool = []
        self._used = []

    def get_connection(self) -> sqlite3.Connection:
        for conn in self._pool:
            if conn not in self._used:
                self._used.append(conn)
                return conn
        if len(self._pool) < self.pool_size:
            conn = sqlite3.connect(self.database_path)
            self._pool.append(conn)
            self._used.append(conn)
            return conn
        raise Exception("All connections are currently in use")

    def release_connection(self, conn: sqlite3.Connection):
        self._used.remove(conn)


class TaxiDataLoader(DataLoader[TaxiData]):

    def __init__(self, start_date: datetime, end_date: datetime, batch_size=10_000, base_path: str="datasets/taxi_dataset/2019/"):
        assert start_date.month == end_date.month, "Date range must be within the same month"
        self.date_from = start_date
        self.date_to = end_date
        self.batch_size = batch_size
        self.base_path = base_path 
        self.filepath = self._construct_filepath()
        self.connection_pool = SQLiteConnectionPool(self.filepath)

    def _construct_filepath(self) -> str:
        """Construct the path based on the month."""
        month = self.date_from.month
        filename = f"2019-{month:02}.sqlite"
        return os.path.join(self.base_path, filename)

    def _connect_to_database(self) -> Optional[sqlite3.Connection]:
        try:
            return self.connection_pool.get_connection()
        except Exception as e:
            print(f"Error when fetching connection from pool: {e}")
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
            self.connection_pool.release_connection(conn)

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
                congestion_surcharge=float(row[17])
            )
        except (ValueError, IndexError):
            return None
