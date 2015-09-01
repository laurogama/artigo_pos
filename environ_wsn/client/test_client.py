import json
import logging
from random import randint
from datetime import datetime
from time import sleep

# from sensors import Sensor
from sensors import Sensor

HOST = '10.8.0.21'
USERNAME = 'sensor_node'
PASSWORD = '123456'
PORT = '5672'
# amqp://user:pass@host:10000/vhost
rabbit_uri = 'amqp://{}:{}@{}:{}'.format(USERNAME, PASSWORD, HOST, PORT)
__author__ = 'laurogama'
# !/usr/bin/env python
import pika

logging.basicConfig()


def random_message(id):
    return {
        "id": id,
        "timestamp": str(datetime.now()),
        "data": {
            "temperature": randint(-40, 80),
            "humidity": randint(1, 99),
            # "ilumination": randint(1, 300),
            # "noise": randint(1, 300),
            # "carbon_monoxide": randint(1, 300),
        }
    }


def send_message(id, data=None):
    if data is None:
        message = json.dumps(random_message(id))
    else:
        message = data
        message['id'] = id
        message['timestamp'] = str(datetime.now())
        message = json.dumps(message)
        print message

    channel.basic_publish(exchange='logs',
                          routing_key=routing_key,
                          body=message)
    print " [x] Sent %r:%r" % (routing_key, message)


def create_rabbitmq_connection():
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=HOST, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs',
                             type='fanout')
    return connection, channel


def collect_data(id):
    msg_counter = 0
    try:
        sensors = Sensor()
        while True:
            sensor_response = sensors.read_sensors()
            send_message(id, sensor_response)
            msg_counter += 1
            sleep(2)
    except KeyboardInterrupt:
        print "messages sent: {}".format(msg_counter)
        connection.close()


def create_fake_data(id):
    msg_counter = 0
    try:
        while True:
            send_message(id)
            msg_counter += 1
            sleep(2)
    except KeyboardInterrupt:
        print "messages sent: {}".format(msg_counter)
        connection.close()


if __name__ == '__main__':
    routing_key = 'anonymous.info'
    connection, channel = create_rabbitmq_connection()
    collect_data(1)
    # create_fake_data(1)
