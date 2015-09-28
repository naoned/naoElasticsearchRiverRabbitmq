# naoRabbitMQRiver

This service simulate a RabbitMQ river for ElasticSearch

It allows to index / update / delete documents in ElasticSearch from a RabbitMQ exchange
The format of messages needs to be in bulk api format :
https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html


# Requirements

Python install:

    $ sudo apt-get install python-setuptools git-core
    $ sudo easy_install pip

Pika install:

    $ pip install pika

or

    $ easy_install pika

# First test and simple run

In a terminal, launch the service :

    $ python bin/naoRiver.py

Send a test message to test the service (this message will not be send to ElasticSearch) :

	$ python test/send.py [your message]

# Daemonize

This command install all the files needed by the service :

    $ ./install.sh

Then you can start/stop the daemon :

    $ /etc/init.d/nao-elastic-river-rabbitmq (start|stop|restart|status)
