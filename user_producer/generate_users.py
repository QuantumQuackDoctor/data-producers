import random, bcrypt, string
from faker import Faker
from user import User
from dao import *
from config import *

fake = Faker()
global_config = config(section='postgresql-prod')

def generatePassword(size=10, chars=string.ascii_letters + string.digits + string.punctuation):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_user():
    id = int(fake.numerify(text='###########'))
    activated = True
    activation_token = fake.uuid4()
    activation_token_expiration = fake.future_datetime(end_date='+30d')
    birth_date = fake.date_of_birth(minimum_age=16, maximum_age=200)
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_symbols = ['','_','.']
    email = first_name.lower() + random.choice(email_symbols) + last_name.lower() + str(fake.random_digit_or_empty()) + '@' + fake.email().split('@')[1]
    is_veteran = random.choice([True, False])
    password = bcrypt.hashpw('password'.encode("utf-8"), bcrypt.gensalt())
    phone = fake.phone_number()
    points = random.randint(0, 100)
    email_option = False
    phone_option = False
    dark = random.choice([True, False])
    email_order = random.choice([True, False])
    email_delivery = False

    return User(id, activated, activation_token, activation_token_expiration, birth_date, email, 
                first_name, is_veteran, last_name, str(password), phone, points, email_option, phone_option, dark, email_order, email_delivery)

def add_user_to_db():
    user = generate_user()
    log.info(user.toDict())
    prepare_statement(CrudOperation.CREATE, 'user_entity', config=global_config, **user.toDict())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    for i in range(1000):
        try:
            add_user_to_db()
        except Exception:
            log.warn('skipping %d',i)