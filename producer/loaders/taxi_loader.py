from datetime import datetime
from typing import Iterator, List, Optional, Tuple
import os
import sqlite3
from dateutil.parser import parse as date_parse
from models.taxi_data import TaxiData
from loaders.interface import DataLoader
from utils.minio import download_objects

class TaxiDataLoader(DataLoader[TaxiData]):

    def __init__(self, start_date: datetime, end_date: datetime, batch_size=10_000, base_path: str="datasets/taxi_dataset/2019/"):
        assert start_date.month == end_date.month, "Date range must be within the same month"
        self.date_from = start_date
        self.date_to = end_date
        self.batch_size = batch_size
        self.base_path = base_path 
        self.filepath = self._construct_filepath()
        
        if not os.path.exists(self.filepath):
            print(f"Downloading Datasets...")
            download_objects()  # Assuming this method is defined to handle the downloading


    def _construct_filepath(self) -> str:
        month = self.date_from.month
        filename = f"2019-{month:02}.sqlite"
        return os.path.join(self.base_path, filename)

    def _connect_to_database(self) -> Optional[sqlite3.Connection]:
        try:
            return sqlite3.connect(self.filepath)
        except sqlite3.Error as e:
            print(f"Error when connecting to the database: {e}")
            return None

    def _execute_query(self, conn: sqlite3.Connection, query: str) -> Iterator[List[Tuple]]:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(query)
                while (batch := cursor.fetchmany(self.batch_size)):
                    yield batch
        except sqlite3.Error as e:
            print(f"SQLite error when executing query: {e}")
        finally:
            cursor.close()
            conn.close()

    def _get_raw_batch(self) -> Iterator[List[Tuple]]:
        query = f"SELECT * FROM tripdata WHERE tpep_pickup_datetime BETWEEN '{self.date_from}' AND '{self.date_to}' ORDER BY tpep_pickup_datetime ASC;"
        conn = self._connect_to_database()
        if conn:
            yield from self._execute_query(conn, query)


    def _parsed_batch(self) -> Iterator[List[TaxiData]]:
        """Iterate over a raw batch and"""
        for raw_batch in self._get_raw_batch():
            parsed_batch = list(filter(None, map(self._from_raw, raw_batch)))
            yield parsed_batch

    def get_entries_in_order(self) -> Iterator[TaxiData]:
        for batch in self._parsed_batch():
            for taxi_data in batch:
                yield taxi_data

    def get_batches(self) -> Iterator[List[TaxiData]]:
        yield from self._parsed_batch()

    def get_avro_schema(self) -> str:
        return TaxiData.avro_schema()

    def _from_raw(self, row) -> Optional[TaxiData]:
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
