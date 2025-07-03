from faker import Faker
from database.database import Database
import random

fake = Faker('Ru_ru')

def create_user():
    full_name = random.choice([fake.name_male(), fake.name_female()])
    phone = '9' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
    client_type = random.choice(['private','legal'])
    company_info = None
    if client_type == 'legal':
        company_info = fake.company()
    return {'full_name':full_name, 'phone':phone, 'client_type':client_type,
            'company_info':company_info}


db = Database()
db.connect('postgres', 79230)

headers = ', '.join(list(create_user().keys()))

db.execute_query()
