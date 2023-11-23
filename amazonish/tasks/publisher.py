import sys
from tasks.views import ProductsCron
import sys
import time

from tasks.views import ProductsCron
import pika


confg = {'host': 'amqps://ccxmvmxb:IM8Q3v7NxDHFHjdNjopIxNPrtxcpm67W@cow.rmq2.cloudamqp.com/ccxmvmxb'}


class Connection():

    def setUpConn(self,confg):
        parameters = pika.URLParameters(confg['host'])
        return pika.BlockingConnection(parameters=parameters)


class RetryingEmailSentsPublisher():
    def __init__(self):
        self.channel = Connection().setUpConn(confg)

    def publishMessage(self):
        channel = self.channel.channel()
        channel.exchange_declare(exchange='dlx', exchange_type='direct')

        channel.queue_declare(queue='dl',
                              arguments={
                                  'x-message-ttl': 5000,
                                  'x-dead-letter-exchange': 'amq.direct',
                                  'x-dead-letter-routing-key': 'task_queue'
                              })

        channel.queue_bind(exchange='dlx', queue='dl')

        print(' [*] Waiting for dead-letters. To exit press CTRL+C')
        channel.queue_declare(queue='task_queue',
                              arguments={
                                  'x-message-ttl': 1000,
                                  'x-dead-letter-exchange': 'dlx',
                                  'x-dead-letter-routing-key': 'dl'
                              }
                              )

        channel.queue_bind(exchange='amq.direct', queue='task_queue')

        print(' [*] Waiting for messages. To exit press CTRL+C')
        
        message = ProductsCron(None).run_task_cron_def()
        print(' [*] Print The Message to be Queued', str(message))

        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=str(message))
        print(" [x] Sent %r" % (message,))
