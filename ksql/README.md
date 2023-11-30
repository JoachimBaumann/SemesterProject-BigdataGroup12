

```bash
kubectl exec --namespace=ksql --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088
```