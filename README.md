# naoRabbitMQRiver

This service simulate a [RabbitMQ](https://www.rabbitmq.com/) river for [ElasticSearch](https://www.elastic.co). This project was created as rivers in ElasticSearch are now [deprecated](https://www.elastic.co/blog/deprecating-rivers).

It allows to index / update / delete documents in ElasticSearch from a RabbitMQ exchange.
The format of messages needs to be in [bulk api format](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)


# Requirements

Please refer to [Python](https://www.python.org) and [Pika](http://pika.readthedocs.org/en/latest/) to install on your own configuration.

Python installon on debian:

    $ sudo apt-get install python-setuptools git-core
    $ sudo easy_install pip

Pika install on debian:

    $ sudo pip install pika

or

    $ sudo easy_install pika


# Firsts tests and simple run

In a terminal, launch the service :

    $ python bin/naoRiver.py

Send a test message to test the service (this message will not be sent to ElasticSearch) :

	$ python test/send.py "your message"

To configure this service with RabbitMQ and ElasticSearch, please see below


# Installation as a service

This command install all the files needed by the service :

    $ sudo ./install.sh

In installation script a user is specified in order to interact with this daemon. In our case it's our web server's user. That's mean our web server can start/stop the service.
If it's not your case, you can choose another user, or disable this functionality with "root" user :

    $ sudo ./install.sh <user>

Then you can start/stop the daemon :

    $ sudo /etc/init.d/nao-elastic-river-rabbitmq (start|stop|restart|status)


# Uninstall

    $ sudo ./uninstall.sh


# Configuration
Configure the service can easily be done by editing the configfile config.json :

    {
    	"RabbitMQ": {
    		"host": "localhost",
    		"port": 5672,
    		"virtual_host": "/",
    		"username": "guest",
    		"password": "guest",
    		"exchange_name": "naoned",
    		"queue_name": "naoned"
    	},
    	"ElasticSearch": {
    		"host": "localhost",
    		"port": "9200"
    	}
    }

If you install the service as a dameon, the location is /opt/nao-elastic-river-rabbitmq/config.json
