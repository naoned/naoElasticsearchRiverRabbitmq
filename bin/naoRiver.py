#!/usr/bin/env python
import pika
import time
import urllib2
import os
import sys
import logging
import datetime

dir = os.path.dirname(os.path.realpath(__file__)) + "/.."

### Import lib
sys.path.append(os.path.abspath(dir))
from lib.RabbitMQConnexion import *
from lib.Config import *
from lib.Logs import *

LOGGER = configureLog(dir)

# Config
config = read_config("{0}/config.json".format(dir))
elasticBulkUrl = 'http://{0}:{1}/_bulk'.format(config["ElasticSearch"]["host"], config["ElasticSearch"]["port"])
stateFile = dir + "/.state.lock"

# Only one instance of this script could run at once. Otherwise who get message?
if os.path.isfile(stateFile):
	LOGGER.error("Error: an instance of this script is already running")
	sys.exit(1)
os.mknod(stateFile)

LOGGER.info('Start naoRiver')

# Connection to RabbitMQ
RMQConnexion = RabbitMQConnection(config["RabbitMQ"])
RMQConnexion.setLogger(LOGGER)
RMQConnexion.connect()

# Execution
try:
	while os.path.isfile(stateFile):

		method_frame, header_frame, msg = RMQConnexion.getMessage()

		if method_frame:
			LOGGER.info('Message received [%s]', msg)
			if method_frame.routing_key != "test":
					try:
						req = urllib2.Request(elasticBulkUrl, data=msg, headers={'Content-type': 'text/plain'})
						response = urllib2.urlopen(req)
					except:
						LOGGER.error("Bad request with message: %s", msg)

			else:
				LOGGER.error("Message is received in test mode: %s", msg)
			RMQConnexion.ackMessage(method_frame.delivery_tag)

		else:
			time.sleep(1)

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:
	LOGGER.info("Interrupt by keyboard")

# Close properly
RMQConnexion.close()

if os.path.isfile(stateFile):
	os.remove(stateFile)

LOGGER.info('Stop naoRiver')
