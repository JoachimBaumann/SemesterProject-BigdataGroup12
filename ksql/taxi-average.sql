CREATE TABLE taxi_average
    WITH (KAFKA_TOPIC='taxi-average', VALUE_FORMAT='JSON') AS
    SELECT
        1,
        AVG(trip_distance) AS AVG_DISTANCE,
        COUNT(*) AS TOTAL_TRIPS,
        AVG(tip_amount) AS AVG_TIP
    FROM taxi_transformed
    WINDOW HOPPING (SIZE 60 MINUTES, ADVANCE BY 10 SECONDS)
    GROUP BY 1
    EMIT FINAL;
