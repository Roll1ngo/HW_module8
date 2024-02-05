import sys
import os

import pika

from models import Contact


def main():
    credentials = pika.PlainCredentials('jbkealrg', '6X3619RfRB0hRckBV7tg0j4YFlzdkZW_')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='kangaroo-01.rmq.cloudamqp.com',
                                  port=5672, credentials=credentials,
                                  virtual_host='jbkealrg'))

    channel = connection.channel()

    queue_name = 'HomeWork remote queue SMS'
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        take_task = Contact.objects(id=pk, sendtosms=True).first()

        if take_task:
            take_task.update(set__is_sended=True)
            print(f"{take_task.phone} {take_task.fullname}: sms send")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
