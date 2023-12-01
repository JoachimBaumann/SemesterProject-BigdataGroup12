CREATE STREAM taxi_transformed 
WITH (KAFKA_TOPIC='taxi-transformed', VALUE_FORMAT='JSON') AS
SELECT 
    tip_amount as tip_amount, 
    trip_distance as trip_distance, 
    vendorid as vendorid, 
    pu_geo_id as pu_geo_id, 
    do_geo_id as do_geo_id
FROM taxi_transformed_intermediate
PARTITION BY pu_geo_id;
