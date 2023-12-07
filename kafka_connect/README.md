# Local deployment

Here is how to apply the kafka connect configuration defined in the kafka-connect.yaml file

```bash
kubectl apply -f kafka-connect.yaml -n kafka
```

Now we need to post the configuration using curl in a terminal with port-forwarding enabled, so:

```bash
kubectl port-forward svc/kafka-connect 8083:8083 -n kafka-connect
```

Run the command below to post the configuration:

1. Apply taxi-data sink
```bash 
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "timescale-sink-taxi",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "auto.evolve": "true",
    "auto.create": "true",
    "tasks.max": "1",
    "insert.mode": "insert",
    "topics": "taxi-data",
    "connection.url": "jdbc:postgresql://timescaledb.timescale.svc.cluster.local:5432/postgres",
    "connection.user": "admin",
    "connection.password": "assword",
    "connection.loginTimeout": "10",
    "key.converter.schemas.enable": "true",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schema.registry.url": "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081",
    "value.converter.schemas.enable": "true",
    "value.converter.schema.registry.url": "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081",
    "value.converter": "io.confluent.connect.avro.AvroConverter"
  }
}' http://127.0.0.1:8083/connectors


curl -X DELETE http://127.0.0.1:8083/connectors/timescale-sink-bus

```

2. Apply bus-data sink
``` bash
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "timescale-sink-bus",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "auto.evolve": "true",
    "auto.create": "true",
    "tasks.max": "1",
    "insert.mode": "insert",
    "topics": "bus-data",
    "connection.url": "jdbc:postgresql://timescaledb.timescale.svc.cluster.local:5432/postgres",
    "connection.user": "admin",
    "connection.password": "assword",
    "connection.loginTimeout": "10",
    "key.converter.schemas.enable": "true",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schema.registry.url": "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081",
    "value.converter.schemas.enable": "true",
    "value.converter.schema.registry.url": "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081",
    "value.converter": "io.confluent.connect.avro.AvroConverter"
  }
}' http://127.0.0.1:8083/connectors

```



To list all connecters run the following:

```bash
curl -X GET http://127.0.0.1:8083/connectors
```


To delete the sink run the following command:

```bash
curl -X DELETE http://127.0.0.1:8083/connectors/hdfs-sink-bus
```


    
