
# Install TimescaleDB
A small guide on how to install timescaledb in kubernetes taken from the docs. 


## Add helm chart
```bash
helm repo add timescale 'https://charts.timescale.com'
helm repo update
```

## Install RimescaleDB in the timescale namespace with value files. 
```bash
kubectl create namespace timescale
helm install timescaledb -f values.yaml timescale/timescaledb-single -n timescale
```

## Connect to TimescaleDB
To get your password for superuser run:

1. Get password from secrets
  ```bash
      PGPASSWORD_ADMIN=$(kubectl get secret --namespace timescale "timescaledb-credentials" -o jsonpath="{.data.PATRONI_admin_PASSWORD}" | base64 --decode)
  ```

2. (a) Run a postgres pod and connect using the psql cli:

    ```bash
    kubectl run -i --tty --rm psql --image=postgres \
      --env "PGPASSWORD=$PGPASSWORD_ADMIN" \
      --command -- psql -U admin \
      -h timescaledb.timescale.svc.cluster.local postgres
    ```

2. (b) Directly execute a psql session on the master node

```bash
MASTERPOD="$(kubectl get pod -o name --namespace timescale -l release=timescaledb,role=master)"
   kubectl exec -i --tty --namespace timescale ${MASTERPOD} -- psql -U postgres
```


Use in other applications: 

Connection string:
postgresql://admin:assword@timescaledb.timescale.svc.cluster.local:5432/postgres


