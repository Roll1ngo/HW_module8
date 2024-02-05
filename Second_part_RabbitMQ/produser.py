import random

from faker import Faker
import pika

from models import Contact

credentials = pika.PlainCredentials('jbkealrg', '6X3619RfRB0hRckBV7tg0j4YFlzdkZW_')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='kangaroo-01.rmq.cloudamqp.com',
                              port=5672, credentials=credentials,
                              virtual_host='jbkealrg'))

channel = connection.channel()

fake = Faker('Uk-ua')
email_exchange = 'HomeWork remote service Email'
email_queue_name = 'HomeWork remote queue Email'

channel.exchange_declare(exchange=email_exchange, exchange_type='direct')
channel.queue_declare(queue=email_queue_name, durable=True)
channel.queue_bind(exchange=email_exchange, queue=email_queue_name)

sms_exchange = 'HomeWork remote service SMS'
sms_queue_name = 'HomeWork remote queue SMS'

channel.exchange_declare(exchange=sms_exchange, exchange_type='direct')
channel.queue_declare(queue=sms_queue_name, durable=True)
channel.queue_bind(exchange=sms_exchange, queue=sms_queue_name)


def create_contacts(nums: int):
    for task in range(nums):
        is_email = random.choice([True, False])
        is_sms = not is_email
        contact = Contact(fullname=fake.name(),
                          email=fake.email(),
                          phone=fake.phone_number(),
                          address=fake.address(),
                          sendtoemail=is_email, sendtosms=is_sms)
        contact.save()
        if is_email is True:
            channel.basic_publish(exchange=email_exchange,
                                  routing_key=email_queue_name,
                                  body=str(contact.id).encode())
        else:  # is_sms is True
            channel.basic_publish(exchange=sms_exchange,
                                  routing_key=sms_queue_name,
                                  body=str(contact.id).encode())

    connection.close()


if __name__ == '__main__':
    create_contacts(20)
