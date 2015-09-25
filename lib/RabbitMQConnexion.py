import pika
import logging

LOGGER = logging.getLogger(__name__)
hdlr = logging.FileHandler('/var/log/nao-elastic-river-rabbitmq.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr) 
ch.setFormatter(formatter)
LOGGER.addHandler(ch) 
LOGGER.setLevel(logging.WARNING)

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
        try:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self._host,
                port=self._port,
                virtual_host=self._vitual_host,
                credentials=self._credentials))
        except:
            LOGGER.error("Connexion to RabbitMQ failed")
            return 0

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
