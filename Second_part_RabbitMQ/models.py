from mongoengine import *

connect(
    db="DB_for_RabbitMQ",
    host="mongodb+srv://Vladislav_B:dIvg5BCNadnWGk7E@hwmongobase.o1jywze.mongodb.net/?retryWrites=true&w=majority"
)


class Contact (Document):
    fullname = StringField(max_length=150)
    email = StringField(max_length=50)
    phone = StringField(max_length=50)
    address = StringField(max_length=500)
    sendtoemail = BooleanField(default=False)
    sendtosms = BooleanField(default=False)
    is_sended = BooleanField(default=False)





