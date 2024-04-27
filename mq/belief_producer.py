import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='belief', durable=True)


def produce_test_message():
    channel.basic_publish(
        exchange='', routing_key='belief', body='Test_message')
    print(" [x] Sent test message")
