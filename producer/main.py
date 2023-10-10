from confluent_kafka import Producer
import socket



conf = {'bootstrap.servers': 'pkc-abcd85.us-west-2.aws.confluent.cloud:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '<CLUSTER_API_KEY>',
        'sasl.password': '<CLUSTER_API_SECRET>',
        'client.id': socket.gethostname()}

producer = Producer(conf)