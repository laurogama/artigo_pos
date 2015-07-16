import json
import logging
from datetime import datetime

from flask import Flask
import pika
from pika.exceptions import AMQPConnectionError

app = Flask(__name__)
QUEUES = ['sensors']
EXCHANGES = [{"name": 'logs', "type": 'fanout'}]

logging.basicConfig()


@app.route('/')
def hello_world():
    return 'Hello World!'


def queue_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    message = json.loads(body)
    message['received_timestamp'] = datetime.now()
    print(message)


def declare_exchanges(channel, exchanges):
    result = channel.queue_declare(exclusive=True)
    for new_exchange in exchanges:
        channel.exchange_declare(exchange=new_exchange['name'],
                                 type=new_exchange['type'])
        channel.queue_bind(
            exchange=new_exchange['name'], queue=result.method.queue)

    channel.basic_consume(queue_callback, queue=result.method.queue,
                          no_ack=True)
    channel.start_consuming()


def connect_to_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()
        declare_exchanges(channel, EXCHANGES)
        return True
    except AMQPConnectionError:
        print("Couldn't connect to RabbitMQ Broker")
        return False


if __name__ == '__main__':
    if connect_to_rabbitmq():
        print("Connected to rabbitmMQ Broker")
        app.run()
