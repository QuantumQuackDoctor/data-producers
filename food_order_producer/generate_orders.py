import random
from faker import Faker
from datetime import timedelta
from order import *
from dao import *
from config import *

fake = Faker()
global_config = config(section='postgresql-prod')

# get user and driver ids
def get_ids():
    user_data = prepare_statement(CrudOperation.READ, 'user_entity', config=global_config)
    driver_data = prepare_statement(CrudOperation.READ, 'driver_entity', config=global_config)
    user_id = ''
    driver_id = ''
    if user_data and driver_data:
        user_ids = [user[0] for user in user_data]
        driver_ids = [driver[1] for driver in driver_data]
        user_id = random.choice(user_ids)
        driver_id = random.choice(driver_ids)
    else:
        log.error('There are no available users or drivers to choose from')
        raise Exception('There are no available users or drivers to choose from')
    log.debug('driver id: %s, user id: %s',driver_id, user_id)
    return (driver_id, user_id)

def generate_order():
    print('here')
    id = int(fake.numerify(text='###########'))
    active = random.choice([True, False])
    geolocation = fake.local_latlng(country_code='US')
    address = fake.street_address() + '\n' + geolocation[2] + ', ' + geolocation[3]
    placed = fake.date_time_between(start_date='-30d', end_date='now')
    food_price = round(random.uniform(5,120), 2)
    payment_confirmed = random.choice([True, False])
    restaurant_accept = fake.date_time_between_dates(datetime_start=placed, datetime_end=placed+timedelta(minutes=40)) if payment_confirmed else None
    restaurant_start = fake.date_time_between_dates(datetime_start=restaurant_accept, datetime_end=restaurant_accept+timedelta(minutes=40)) if payment_confirmed else None
    restaurant_complete = fake.date_time_between_dates(datetime_start=restaurant_start, datetime_end=restaurant_start+timedelta(minutes=40)) if payment_confirmed else None
    delivery = random.choice([True, False]) if payment_confirmed else None
    ids = get_ids()
    driver_user_id = ids[0] if delivery else None
    delivery_price = round(random.uniform(3,10), 2) if delivery else None
    driver_accept = fake.date_time_between_dates(datetime_start=restaurant_accept, datetime_end=restaurant_complete) if delivery else None
    driver_note = fake.paragraph() if delivery else None
    delivery_slot = fake.date_time_between_dates(datetime_start=restaurant_complete, datetime_end=restaurant_complete+timedelta(minutes=40)) if delivery else None
    driver_complete = fake.date_time_between_dates(datetime_start=restaurant_complete, datetime_end=restaurant_complete+timedelta(minutes=40)) if delivery else None
    tip = round(random.uniform(0,50), 2) if delivery else None
    order_complete = ''
    try:
        order_complete = fake.date_time_between_dates(datetime_start=driver_complete, datetime_end=driver_complete+timedelta(minutes=50)) if delivery else None
    except Exception:
        order_complete = driver_complete if delivery else None
    refunded = random.choice([True, False]) if payment_confirmed else False
    restaurant_note = fake.paragraph()
    user_id = ids[1]
    confirmation_code = fake.bothify('########') if payment_confirmed else None
    order = Order(id, active, address, delivery, driver_note, delivery_slot, driver_accept, driver_complete, order_complete,
                 placed, restaurant_accept, restaurant_complete, restaurant_start, delivery_price, food_price,
                 tip, refunded, restaurant_note, driver_user_id, user_id, confirmation_code, payment_confirmed)
    print(**order.toDict())
    log.info('order: %s', **order.toDict())

    return order


# generates food order by using order id and restaurant id
def gen_food_order(order_id):
    restaurant_data = prepare_statement(CrudOperation.READ, 'restaurant_entity', config=global_config)
    restaurant_id = ''
    if restaurant_data:
        restaurant_ids = [restaurant[0] for restaurant in restaurant_data]
        restaurant_id = random.choice(restaurant_ids)
    else:
        raise Exception('There are no available restaurants to choose from')

    log.debug('order id: %s, restaurant id: %s', order_id, restaurant_id)
    return {
        'id': order_id,
        'restaurant_id': restaurant_id
    }

def gen_order_item(order_id):
    menu_data = prepare_statement(CrudOperation.READ, 'menu_item_entity', config=global_config)
    if menu_data:
        menu_ids = [menu[0] for menu in menu_data]
        menu_id = random.choice(menu_ids)
    else:
        log.error('There are no available menu items to choose from')
        raise Exception('There are no available menu items to choose from')
    
    log.debug('menu id: %s, order id: %s', menu_id, order_id)
    return {
        'order_items_id': menu_id,
        'food_order_entity_id': order_id
    }

# add order to db
def add_order_to_db():
    order = generate_order()
    item_id = int(fake.numerify(text='###########'))
    
    # add order to db
    log.info('Adding %s to order_entity table', **order.toDict())
    prepare_statement(CrudOperation.CREATE, 'order_entity', config=global_config, **order.toDict())

    # links order items with nmenu items through food_order_entity_order_items table
    # food_order = gen_food_order(item_id)
    # log.info('Adding %s to food_order_entity table', **food_order)
    # prepare_statement(CrudOperation.CREATE, 'food_order_entity', config=global_config, **food_order)

    # # food_order_entity_order_items table links a menu id with order id
    # order_item = gen_order_item(item_id)
    # log.info('Adding %s to food_order_entity_order_items table', **order_item)
    # prepare_statement(CrudOperation.CREATE, 'food_order_entity_order_items', config=global_config, **order_item)

    # # links order with menu item through food_order_entity and food_order_entity_order_items
    # order_entity_items = lambda o, i: {'order_entity_id': o, 'items_id': i}
    # log.info('Adding to order_entity_items table', **order_entity_items(order.id, item_id))
    # prepare_statement(CrudOperation.CREATE, 'order_entity_items', config=global_config, **order_entity_items(order.id, item_id))

    # # generates db format for user_entity_order_list: links user id with order id
    # gen_user_order = lambda user_id, order_id: {'user_entity_id': user_id,  'order_list_id': order_id}
    # log.info('Adding %s to user_entity_order_list table', **gen_user_order(order.user_id, order.id))
    # prepare_statement(CrudOperation.CREATE, 'user_entity_order_list', config=global_config, **gen_user_order(order.user_id, order.id))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    for i in range(50):
        try:
            add_order_to_db()
        except Exception:
            log.warn('skipping %s', str(i))