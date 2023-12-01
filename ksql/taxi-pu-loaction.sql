CREATE TABLE taxi_pu_location
WITH (KAFKA_TOPIC='taxi-pu-location', VALUE_FORMAT='JSON', KEY_FORMAT='JSON') AS
SELECT pu_geo_id, AVG(trip_distance) AS avg_distance, COUNT(*) AS total_trips, AVG(tip_amount) AS avg_tip
FROM taxi_transformed
WINDOW HOPPING (SIZE 60 MINUTES, ADVANCE BY 10 SECONDS)
GROUP BY pu_geo_id
EMIT FINAL;