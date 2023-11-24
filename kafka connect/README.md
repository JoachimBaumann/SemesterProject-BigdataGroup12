# Local deployment

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

To run a based version that takes avro instead of json use the following script:

```
$body = @{
    name = "hdfs-sink-taxi"
    config = @{
        "connector.class" = "io.confluent.connect.hdfs.HdfsSinkConnector"
        "tasks.max" = "5"
        "topics" = "taxi-data"
        "hdfs.url" = "hdfs://simple-hdfs-namenode-default-1.default:8020"
        "flush.size" = "3"
        "format.class" = "io.confluent.connect.hdfs.avro.AvroFormat"
        "key.converter.schemas.enable" = "true"
        "key.converter" = "org.apache.kafka.connect.storage.StringConverter"
        "key.converter.schema.registry.url" = "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081"
        "value.converter.schemas.enable" = "true"
        "value.converter.schema.registry.url" = "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081"
        "value.converter" = "io.confluent.connect.avro.AvroConverter"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri 'http://127.0.0.1:8083/connectors' -Method Post -ContentType 'application/json' -Body $body
```

To create the bus data connector:

```
$body = @{
    name = "hdfs-sink-bus"
    config = @{
        "connector.class" = "io.confluent.connect.hdfs.HdfsSinkConnector"
        "tasks.max" = "5"
        "topics" = "bus-data"
        "hdfs.url" = "hdfs://simple-hdfs-namenode-default-1.default:8020"
        "flush.size" = "3"
        "format.class" = "io.confluent.connect.hdfs.avro.AvroFormat"
        "key.converter.schemas.enable" = "true"
        "key.converter" = "org.apache.kafka.connect.storage.StringConverter"
        "key.converter.schema.registry.url" = "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081"
        "value.converter.schemas.enable" = "true"
        "value.converter.schema.registry.url" = "http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081"
        "value.converter" = "io.confluent.connect.avro.AvroConverter"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri 'http://127.0.0.1:8083/connectors' -Method Post -ContentType 'application/json' -Body $body
```

To list all connecters run the following:

```
Invoke-RestMethod -Uri 'http://127.0.0.1:8083/connectors' -Method Get
```

Run diagnostics

```
Invoke-RestMethod -Uri 'http://127.0.0.1:8083/connectors/hdfs-sink-taxi/status' -Method Get
$response = Invoke-RestMethod -Uri 'http://127.0.0.1:8083/connectors/hdfs-sink-taxi/status' -Method Get
$response | ConvertTo-Json | Out-String | Out-File -FilePath "connector_status.json"


```

To delete the sink run the following command:

```
Invoke-RestMethod -Method Delete -Uri 'http://127.0.0.1:8083/connectors/hdfs-sink-taxi'
```

# IMPORTANT

The image Anders gave us only writes to the namenode that ends with a -1 instead of -0. In case you run into a situation where our namenodes comes back from a failure and as such have switched jobs you have to force them to switch back in order for the sinks to work. Ssh into the hdfs-cli pod and run the following command:

```
hdfs haadmin -failover simple-hdfs-namenode-default-0 simple-hdfs-namenode-default-1
```
