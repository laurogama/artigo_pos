import logging

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


def create_queues(channel, queues):
    for new_queue in queues:
        channel.queue_declare(queue=new_queue)
        channel.basic_consume(queue_callback,
                              queue=new_queue)


def queue_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def declare_exchanges(channel, exchanges):
    with channel.queue_declare(exclusive=True) as result:
        for exchange in exchanges:
            channel.exchange_declare(exchange=exchange.name,
                                     type=exchange.type)
            channel.queue_bind(exchange=exchange.name,
                               queue=result.method.queue)
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
        app.run()
