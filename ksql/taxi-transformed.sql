CREATE STREAM taxi_transformed 
   WITH (KAFKA_TOPIC='taxi-transformed', VALUE_FORMAT='JSON') AS
   SELECT
   CASE
       WHEN pulocationid = 1 THEN 'a'
       WHEN pulocationid = 2 THEN 'b'
       WHEN pulocationid = 3 THEN 'c'
       WHEN pulocationid = 4 THEN 'd'
       WHEN pulocationid = 5 THEN 'e'
       ELSE 'unknown'
   END AS pu_geo_id
   FROM taxi_data;
