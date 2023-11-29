# Trino with hive with hdfs

## 1. Setup

Install postgresql:

```powershell
helm install postgresql --version=12.1.5 --set auth.username=hive --set auth.password=hive --set auth.database=hive --set primary.extendedConfiguration="password_encryption=md5" --repo https://charts.bitnami.com/bitnami postgresql

```

PostgreSQL can be accessed via port 5432

Unix:

```bash
kubectl port-forward --namespace default svc/postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U hive -d hive -p 5432
```

Windows:

```powershell
kubectl port-forward svc/postgresql 5432:5432
psql --host 127.0.0.1 -U hive -d hive -p 5432
```

Apply the trino and hive files file that contains the cluster and the catalog that links to hdfs:

```powershell
kubectl apply -f hive.yaml
kubectl apply -f trino.yaml
```
