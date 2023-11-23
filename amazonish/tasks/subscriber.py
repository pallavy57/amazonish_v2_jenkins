
import pika


confg = {"host": 'amqps://ccxmvmxb:IM8Q3v7NxDHFHjdNjopIxNPrtxcpm67W@cow.rmq2.cloudamqp.com/ccxmvmxb'}


class Connection():
    def setUpConn(self, confg):
        parameters = pika.URLParameters(confg['host'])
        return pika.BlockingConnection(parameters=parameters)


class RetryingEmailSentsConsumer():
    def __init__(self):
        self.channel = Connection().setUpConn(confg)

    def callback(self, ch, method, properties, body):
          try:
        # Your processing logic here
                print("Processing message:", body)
                
          except Exception as e:
                # If processing fails, requeue the message
                print("Message processing failed:", e)
                print('retry count', properties.headers['x-retry-count'])
                if properties.headers.get('x-death') == None or properties.headers['x-retry-count'] < 5:
                    ch.basic_reject(
                        delivery_tag=method.delivery_tag, requeue=False)
                    print(" [x] Rejected")
                else:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(" [x] Timed out")

    def consumer_e(self):
        channel = self.channel.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue',
                              on_message_callback=self.callback, auto_ack=False)


        
        try:
            channel.start_consuming()
        except pika.exceptions.ChannelClosedByBroker:
            # Lock not acquired, exit
            return
