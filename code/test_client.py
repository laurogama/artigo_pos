import json
import logging

__author__ = 'laurogama'
# !/usr/bin/env python
import pika
import sys

logging.basicConfig()

message = {
    "id": "123u9u8y3873979739739643867321",
    "data": {
        "temperature": 35,
        "ilumination": 210
    }
}

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or json.dumps(message)
channel.basic_publish(exchange='logs',
                      routing_key=routing_key,
                      body=message)
print " [x] Sent %r:%r" % (routing_key, message)
connection.close()
