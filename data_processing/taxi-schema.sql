CREATE STREAM taxi_data 
WITH (
    KAFKA_TOPIC='taxi-data',
    VALUE_FORMAT='AVRO',
);
