CREATE TABLE taxi_average
WITH (KAFKA_TOPIC='taxi-average', VALUE_FORMAT='JSON') AS
SELECT 1, AVG(trip_distance) AS avg_distance, COUNT(*) AS total_trips, AVG(tip_amount) AS avg_tip
FROM taxi_data
WINDOW HOPPING (SIZE 60 MINUTES, ADVANCE BY 10 SECONDS)
GROUP BY 1
EMIT FINAL;
