CREATE STREAM bus_data WITH (
    KAFKA_TOPIC='bus-data',
    VALUE_FORMAT='AVRO'
);

CREATE STREAM bus_json 
  WITH (KAFKA_TOPIC='bus-json', VALUE_FORMAT='JSON') AS 
  SELECT * FROM bus_data;  