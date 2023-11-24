from datetime import timezone
import time
from typing import List, Literal, Union
from loaders.interface import DataLoader
from models.interfaces import Data
from utils.window import sliding_window
import requests
import json
from dataclasses import asdict


from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry.avro import AvroSerializer

def to_dict(busdata: Data, ctx):
    
    return asdict(busdata)

class DataSender:

    def __init__(self, loader: DataLoader[Data], producer, schema_client, topic: str ) -> None:
        self.loader = loader
        self.producer = producer
        self.schema_client = schema_client
        self.topic = topic
        
        self.avro_serializer = AvroSerializer(schema_client,
                                loader.get_avro_schema(),
                                to_dict)
        
        self.string_serializer = StringSerializer('utf_8')
        

    def _send(self, data: Data):
        """Send a single entry to kafka"""
        utc_milliseconds_time = int(data.timestamp.replace(tzinfo=timezone.utc).timestamp() * 1000)
        self.producer.produce(self.topic, 
                              key=self.string_serializer(data.unique_identifier), 
                              value=self.avro_serializer(data, SerializationContext(self.topic, MessageField.VALUE)), 
                              timestamp=utc_milliseconds_time)
        self.producer.flush()

    def _send_batch(self, batch: List[Data]):
        """Send a batch of data entries to kafka"""
        for data in batch:
            utc_milliseconds_time = int(data.timestamp.replace(tzinfo=timezone.utc).timestamp() * 1000)
            self.producer.produce(self.topic, key=data.unique_identifier, value=data.serialize(), timestamp=utc_milliseconds_time)
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
            
            self._send(current)

            if sleep_duration > 2.0:
                print("sleeping for", sleep_duration, "seconds...")
            
            time.sleep(sleep_duration)
