#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='naoned', type='fanout')

message = ' '.join(sys.argv[1:]) or '{ "index" : { "_index" : "test", "_type" : "type1", "_id" : "1" } }{ "field1" : "value1" }'
channel.basic_publish(exchange='naoned', routing_key='test', body=message)

print " [x] Sent %r" % (message,)

connection.close()
