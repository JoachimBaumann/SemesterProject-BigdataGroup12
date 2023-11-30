CREATE STREAM taxi_data WITH (
    KAFKA_TOPIC='taxi-data',
    VALUE_FORMAT='AVRO'
);

CREATE STREAM taxi_json
  WITH (KAFKA_TOPIC='taxi-json', VALUE_FORMAT='JSON', KEY_FORMAT='JSON') AS
  SELECT *
  FROM taxi_data
  PARTITION BY pulocationid;