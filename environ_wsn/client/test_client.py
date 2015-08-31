import json
import logging
from random import randint
from datetime import datetime
from time import sleep

from sensors import Sensor

__author__ = 'laurogama'
# !/usr/bin/env python
import pika

logging.basicConfig()


def random_message(id=None):
    return {
        "id": id,
        "timestamp": str(datetime.now()),
        "data": {
            "temperature": randint(1, 100),
            "humidity": randint(1, 300),
            "ilumination": randint(1, 300),
            "noise": randint(1, 300),
            "carbon_monoxide": randint(1, 300),
        }
    }


def send_message(id, sensor_data):
    message = {"data": sensor_data}
    message = json.dumps(random_message(id))

    channel.basic_publish(exchange='logs',
                          routing_key=routing_key,
                          body=message)
    print " [x] Sent %r:%r" % (routing_key, message)


def create_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs',
                             type='fanout')
    return connection, channel


if __name__ == '__main__':
    connection, channel = create_rabbitmq_connection()
    msg_counter = 0
    try:
        routing_key = 'anonymous.info'
        sensors = Sensor()
        last_data = datetime.now()
        while True:
            sensor_response = sensors.read_sensors()
            if last_data > sensor_response['timestamp']:
                send_message(msg_counter, sensor_response)
                last_data = sensor_response['timestamp']
                msg_counter += 1
            sleep(2)
    except KeyboardInterrupt:
        print "messages sent: {}".format(msg_counter)
        connection.close()
