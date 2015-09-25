#!/usr/bin/env python
import pika
import time
import urllib2
import json
import os
import sys

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

RMQConnexion = RabbitMQConnection(config["RabbitMQ"])
RMQConnexion.connect()

print 'Naoned river starts !'
print ' [*] Waiting for messages. To exit press CTRL+C'

# def callback(ch, method, properties, body):
#     print " [x] %r" % (body,)

try:
	while True:

		#method_frame, header_frame, msg = channel.basic_get(queue_name)
		method_frame, header_frame, msg = RMQConnexion.getMessage()

		if method_frame:
			if method_frame.routing_key != "test":
				if is_json(msg):

					print "Send to Elastic !"
					# req = urllib2.Request(elasticBulkUrl, data=msg, headers={'Content-type': 'text/plain'})
					# response = urllib2.urlopen(req)
					# # print response.info()

					#urllib2.urlopen(elasticBulkUrl, json_msg)
				else:
					print "Error : message is not a valid JSON. msg = {0}".format(msg)
			else:
				print "Message is received in test mode: {0}".format(msg)
			RMQConnexion.ackMessage(method_frame.delivery_tag)
			
		else:
			time.sleep(1)

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:
	print "close !"
	RMQConnexion.close()
