

```bash
kubectl exec --namespace=kafka --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088
```