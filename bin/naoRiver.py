#!/usr/bin/env python
import pika
import time
import urllib2
import json
import os
import sys
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


### Import lib
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(dir + "/.."))

from lib.RabbitMQConnexion import *
from lib.Config import *

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True


config = read_config("{0}/../config.json".format(dir))
elasticBulkUrl = 'http://{0}:{1}/_bulk'.format(config["ElasticSearch"]["host"], config["ElasticSearch"]["port"])
stateFile = dir + "/../.state.lock"
if os.path.isfile(stateFile):
	LOGGER.error("Error: an instance of this script is already running")
	sys.exit(1)
os.mknod(stateFile)

LOGGER.info('Connexion to RabbitMQ')
RMQConnexion = RabbitMQConnection(config["RabbitMQ"])
RMQConnexion.connect()

print 'Start'
LOGGER.info('Start')

try:
	while os.path.isfile(stateFile):

		method_frame, header_frame, msg = RMQConnexion.getMessage()

		if method_frame:
			LOGGER.info('Message received [%s]', msg)
			if method_frame.routing_key != "test":
				if is_json(msg):

					print "Send to Elastic !"
					# @todo
					# req = urllib2.Request(elasticBulkUrl, data=msg, headers={'Content-type': 'text/plain'})
					# response = urllib2.urlopen(req)
					# # print response.info()

				else:
					LOGGER.error("Error : message is not a valid JSON %s", msg)
			else:
				print "Message is received in test mode: {0}".format(msg)
				OGGER.error("Message is received in test mode: %s", msg)
			RMQConnexion.ackMessage(method_frame.delivery_tag)
			
		else:
			time.sleep(1)

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:
	LOGGER.info("Interrupt by keyboard")

RMQConnexion.close()
LOGGER.info('Stop')

if os.path.isfile(stateFile):
	os.remove(stateFile)
