import json
import logging
from dateutil.parser import parse

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import Model, SQLAlchemy
import pika
from pika.exceptions import AMQPConnectionError
from sqlalchemy import Integer, Column, DateTime

from settings import SQLITE_TEST_DB

app = Flask(__name__)
Bootstrap(app)
QUEUES = ['sensors']
EXCHANGES = [{"name": 'logs', "type": 'fanout'}]
logging.basicConfig()
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_TEST_DB
db = SQLAlchemy(app)


def queue_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    message = json.loads(body)
    try:
        msg = Message(message)
        db.session.add(msg)
        db.session.commit()
    except Exception:
        raise
    print(message)


class Message(db.Model):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    sender = Column(Integer)
    temperature = Column(Integer)
    humidity = Column(Integer)
    noise = Column(Integer)
    ilumination = Column(Integer)
    carbon_monoxide = Column(Integer)

    def __init__(self, message):
        try:
            self.timestamp = parse(message['timestamp'])
            self.sender = message['id']
            self.humidity = message['data']['humidity']
            self.ilumination = message['data']['ilumination']
            self.temperature = message['data']['temperature']
            self.noise = message['data']['noise']
            self.carbon_monoxide = message['data']['carbon_monoxide']
        except:
            raise

    def __repr__(self):
        return "Message {} from {}, at {} ".format(self.id, self.sender,
                                                   self.timestamp)


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


@app.route('/')
def index():
    msgs = Message.query.limit(100).all()
    print(msgs)
    return render_template('show_messages.html', messages=msgs)


if __name__ == '__main__':
    # db.create_all()
    app.run(port=9001)
    if connect_to_rabbitmq():
        print("Connected to rabbitmMQ Broker")
