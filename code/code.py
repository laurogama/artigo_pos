from flask import Flask
import pika
from pika.exceptions import AMQPConnectionError

app = Flask(__name__)
QUEUES = ['sensors']


@app.route('/')
def hello_world():
    return 'Hello World!'


def create_queues(queues):
    for new_queue in queues:
        channel.queue_declare(queue=new_queue)
        channel.basic_consume(queue_callback,
                              queue=new_queue)


def queue_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def connect_to_rabbitmq():
    global channel
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()
        create_queues(QUEUES)
        channel.start_consuming()
        return True
    except AMQPConnectionError:
        print("Couldn't connect to RabbitMQ Broker")
        return False


if __name__ == '__main__':
    if connect_to_rabbitmq():
        app.run()
