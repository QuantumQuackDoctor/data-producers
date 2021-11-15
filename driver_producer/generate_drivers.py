import random
from faker import Faker
from faker_vehicle import VehicleProvider
from driver import *
from dao import *
from config import *
from mock_data import *

fake = Faker()
fake.add_provider(VehicleProvider)
global_config = config(section='postgresql-prod')
log = logging.getLogger(__name__)

# gets a random user id that's not a driver
def get_user_id():
    user_data = prepare_statement(CrudOperation.READ, 'user_entity', config=global_config)
    driver_data = prepare_statement(CrudOperation.READ, 'driver_entity', config=global_config)
    driver_id = ''
    if user_data:
        user_ids = [user[0] for user in user_data]
        if driver_data:
            # get list of users that are not drivers
            available_user_ids = list(set(user_ids).difference([driver[1] for driver in driver_data]))
            if not available_user_ids:
                log.error('There are no available users to be added to drivers')
                raise Exception('There are no available users to be added to drivers')
            driver_id = random.choice(available_user_ids)
        else:
            driver_id = random.choice(user_ids)
    else:
        log.error('There are no available users to be added to drivers')
        raise Exception('There are no available users to be added to drivers')
    return driver_id

def get_driver_id():
    driver_data = prepare_statement(CrudOperation.READ, 'driver_entity', config=global_config)
    if driver_data:
        return random.choice([driver[1] for driver in driver_data])
    else:
        log.error('There are no drivers')
        raise Exception('There are no drivers')

def generate_driver():
    car = fake.vehicle_year() + ' ' + fake.vehicle_make() + ' ' + fake.vehicle_model()
    user_id = get_user_id()
    log.debug(user_id)
    return Driver(car, user_id)

def generate_driver_ratings():
    id = int(fake.numerify(text='###########'))
    description = fake.paragraph()
    stars = random.randrange(0,5)
    driver_id = get_driver_id()
    log.debug(id, description, stars, driver_id)
    return DriverRatings(id, description, stars, driver_id)

def add_driver_to_db():
    driver = generate_driver()
    log.debug(driver)
    prepare_statement(CrudOperation.CREATE, 'driver_entity', config=global_config, **driver.toDict())

def add_driver_rating():
    driver_ratings = generate_driver_ratings()
    log.info('Adding', driver_ratings.toDict(), 'to driver_rating_entity')
    prepare_statement(CrudOperation.CREATE, 'driver_rating_entity', config=global_config, **driver_ratings.toDict())
    drivers_rating = DriversRating(driver_ratings.user_id, driver_ratings.id)
    log.info('Adding', drivers_rating.toDict(), 'to driver_entity_ratings')
    prepare_statement(CrudOperation.CREATE, 'driver_entity_ratings', config=global_config, **drivers_rating.toDict())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    for i in range(1000):
        try:
            add_driver_to_db()
        except Exception:
            log.warn('skipping %s', str(i))
    for i in range(1000):
        try:
            add_driver_rating()
        except Exception:
            log.warn('skipping %s', str(i))