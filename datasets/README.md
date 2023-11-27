#### MinIO

Many of the tools on the Stackable platform integrates with S3 storage. We will primarily be using S3 to store historical data of Spark jobs that can then be viewed using a history server.

MinIO is an S3 compatible object store. It can be deployed using the [bitnami helm chart](https://github.com/bitnami/charts/tree/main/bitnami/minio/).

``` bash
helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set defaultBuckets=spark-logs --set auth.rootUser=admin --set auth.rootPassword=password -n python
```

**Note:** We set the user to `admin` and password to `password` to ensure the username and password are the same. You could use other usernames and passwords but then you need to update the provided files.

MinIO Console is a web interface for MinIO. The port for the console is port `9001`.


**Hint:** 
``` bash
kubectl port-forward svc/minio 9001:9001
```