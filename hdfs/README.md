# Setup HDFS

### 1. Setup HDFS

Do whatever they did in exercise 2

### 2. Seeting what's stored in HDFS

To see the data from the taxi dataset, ssh into the hdfs-cli pod and run the following:

```
hdfs dfs -ls hdfs://simple-hdfs-namenode-default-0:8020/topics/taxi-data/partition=0
```

You might have to change the simple-hdfs-namenode-default-0 to simple-hdfs-namenode-default-1 depending on which namenode is currently active and which one is currently functioning as the backup.
