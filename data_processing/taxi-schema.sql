CREATE STREAM taxi_data (
    vendorid INT,
    tpep_pickup_datetime VARCHAR,
    tpep_dropoff_datetime VARCHAR,
    passenger_count INT,
    trip_distance DOUBLE,
    ratecodeid INT,
    store_and_fwd_flag BOOLEAN,
    pulocationid INT,
    dolocationid INT,
    payment_type INT,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    congestion_surcharge DOUBLE
) WITH (
    KAFKA_TOPIC='taxi-data',
    VALUE_FORMAT='JSON',
    TIMESTAMP='tpep_pickup_datetime',
    TIMESTAMP_FORMAT='yyyy-MM-dd''T''HH:mm:ss'
);
