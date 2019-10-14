import string
import faker

from users.models import User
# from data.models import Computer, ScanningRecord, FileInfo
from django.utils.crypto import get_random_string

from celery import shared_task

from faker import Faker
fake = Faker()

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        companyName = fake.company()   
        companyURL = fake.url(schemes=None)

        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = 'SecurityRabbit'

        User.objects.create_user(username=username, email=email, password=password, companyName=companyName, companyURL=companyURL)
    
    return '{} random users created with success!'.format(total)