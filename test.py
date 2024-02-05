import random
testGH = 'test GH'


def create_contacts(nums: int):
    for task in range(nums):
        is_email = random.choice([True, False])
        print(f'{task} email status - {is_email}')
        is_sms = not is_email
        print(f'{task} sms status - {is_sms}')

create_contacts(3)