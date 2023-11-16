# local deployment

Here is how to apply the kafka connect configuration defined in the kafka-connect.yaml file

```
kubectl apply -f kafka-connect.yaml -n kafka
```

Now we need to post the configuration using curl in a terminal with port-forwarding enabled, so:

```
kubectl port-forward svc/kafka-connect 8083:8083 -n kafka
```

Run the command below to post the configuration:

```
$body = @{
    name = "hdfs-sink"
    config = @{
        "connector.class" = "io.confluent.connect.hdfs.HdfsSinkConnector"
        "tasks.max" = "5"
        "topics" = "taxi-data"
        "hdfs.url" = "hdfs://simple-hdfs-namenode-default-1.default:8020"
        "flush.size" = "3"
        "format.class" = "io.confluent.connect.hdfs.json.JsonFormat"
        "key.converter.schemas.enable" = "false"
        "key.converter" = "org.apache.kafka.connect.storage.StringConverter"
        "key.converter.schema.registry.url" = " http://kafka-schema-registry:8081
"
        "value.converter.schemas.enable" = "false"
        "value.converter.schema.registry.url" = " redpanda-0.redpanda.redpanda.svc.cluster.local:8081
"
        "value.converter" = "org.apache.kafka.connect.json.JsonConverter"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri 'http://127.0.0.1:8083/connectors' -Method Post -ContentType 'application/json' -Body $body
```

