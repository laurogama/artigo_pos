import json

import pika
from pika.exceptions import AMQPConnectionError

from model import Message, create_db_session
from settings import EXCHANGES

__author__ = 'laurogama'
MESSAGE_FIELDS = ['humidity', 'ilumination', 'temperature', 'carbon_monoxide',
                  'noise']


def queue_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    message = json.loads(body)
    try:
        data = message['data']
        for item in MESSAGE_FIELDS:
            if item not in data.keys():
                data[item] = None
        # print message
        msg = Message(message)
        db_session.add(msg)
        db_session.commit()
    except Exception:
        db_session.rollback()
        print "db error"
        raise
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
        print "creating connection"
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()
        declare_exchanges(channel, EXCHANGES)
        return True
    except AMQPConnectionError:
        print("Couldn't connect to RabbitMQ Broker")
        return False


if __name__ == '__main__':
    try:
        db_session = create_db_session()
        if connect_to_rabbitmq():
            print "connected sucessfully"
    except KeyboardInterrupt:
        print "Exiting gracefully"
