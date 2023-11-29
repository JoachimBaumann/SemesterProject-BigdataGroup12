import socket

KAFKA_CONFIG = {
    "bootstrap.servers": "redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093",
    "client.id": socket.gethostname(),
}
