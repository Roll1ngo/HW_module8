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
exchange = 'HomeWork remote service Email'
queue_name = 'HomeWork remote queue Email'

channel.exchange_declare(exchange=exchange, exchange_type='direct')
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_name)


def create_contacts(nums: int):
    for task in range(nums):
        contact = Contact(fullname=fake.name(),
                          email=fake.email(),
                          phone=fake.phone_number(),
                          address=fake.address())
        contact.save()
        channel.basic_publish(exchange=exchange,
                              routing_key=queue_name,
                              body=str(contact.id).encode())

    connection.close()


if __name__ == '__main__':
    create_contacts(5)
