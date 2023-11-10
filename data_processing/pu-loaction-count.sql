CREATE TABLE pu_location_count
WITH (KAFKA_TOPIC='pu-location-count', VALUE_FORMAT='JSON') AS
SELECT pulocationid, AVG(trip_distance) AS avg_distance, COUNT(*) AS total_trips, AVG(tip_amount) AS avg_tip, AVG(pulocationid) AS pickup_location_id
FROM taxi_data
WINDOW HOPPING (SIZE 60 MINUTES, ADVANCE BY 10 SECONDS)
GROUP BY pulocationid
EMIT FINAL;