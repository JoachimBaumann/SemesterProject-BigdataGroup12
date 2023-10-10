from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': '''redpanda-0.redpanda.redpanda.svc.cluster.local:9093,redpanda-1.redpanda.redpanda.svc.cluster.local:9093,redpanda-2.redpanda.redpanda.svc.cluster.local:9093''',
        'client.id': socket.gethostname()}

producer = Producer(conf)

producer.produce("twitch-chat", key="val", value="From python 2.0")
producer.flush()