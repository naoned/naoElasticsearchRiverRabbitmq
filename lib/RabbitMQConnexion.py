import pika
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQConnection(object):
    """This class allows to get a basic RabbitMQ connexion on a particular exchange

    """

    def __init__(self, config):
        self._host = config["host"]
        self._port = config["port"]
        self._vitual_host = config["virtual_host"]
        self._exchange_name = config["exchange_name"]
        self._queue_name = config["queue_name"]
        self._credentials = pika.PlainCredentials(config["username"], config["password"])
        

    def connect(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            virtual_host=self._vitual_host,
            credentials=self._credentials))
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange=self._exchange_name, type='fanout')
        if self._queue_name == "":
            result = self._channel.queue_declare(exclusive=True)
            self._queue_name = result.method.queue
        else:
            self._channel.queue_declare(self._queue_name)
        self._channel.queue_bind(exchange=self._exchange_name, queue=self._queue_name)

        return self._connection

    def getMessage(self):
        return self._channel.basic_get(self._queue_name)

    def ackMessage(self, deliveryTag):
        return self._channel.basic_ack(deliveryTag)

    def close(self):
        self._connection.close()
