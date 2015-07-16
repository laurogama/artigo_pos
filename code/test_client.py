import json
import logging
from random import randint
from datetime import datetime

__author__ = 'laurogama'
# !/usr/bin/env python
import pika
import sys

logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         type='fanout')
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'


def random_message():
    return {
        "id": randint(1, 1000),
        "timestamp": str(datetime.now()),
        "data": {
            "temperature": randint(1, 100),
            "humidity": randint(1, 300),
            "ilumination": randint(1, 300),
            "noise": randint(1, 300),
            "carbon_monoxide": randint(1, 300),
        }
    }


message = ' '.join(sys.argv[2:]) or json.dumps(random_message())
channel.basic_publish(exchange='logs',
                      routing_key=routing_key,
                      body=message)
print " [x] Sent %r:%r" % (routing_key, message)
connection.close()
