import random
from faker import Faker
from restaurant import *
from mock_data import *
from dao import *

fake = Faker()
global_config = config(section='h2')
log = logging.getLogger(__name__)

def generate_image():
    id = ''
    oid = ''
    return Image(id, oid)

def generate_menu(): 
    id = int(fake.numerify(text='###########'))
    name = random.choice(food_items)
    imageId = ''
    allergens = random.choice(food_allergens)
    price = round(random.uniform(5,120), 2)
    description = fake.paragraph()
    return Menu(id, name, imageId, allergens, price, description)

def generate_promotions():
    id = int(fake.numerify(text='###########'))
    condition = random.choice(condition_options)
    discount = round(random.uniform(1,20), 2)
    name = random.choice(discount_types)
    return Promotion(id, condition, discount, name)

def get_user_id():
    user_data = prepare_statement(CrudOperation.READ, 'user_entity', config=global_config)
    restaurant_rating_data = prepare_statement(CrudOperation.READ, 'restaurant_rating_entity', config=global_config)
    user_id = ''
    if user_data:
        user_ids = [user[0] for user in user_data]
        if restaurant_rating_data:
            # get list of users that haven't given a rating
            available_user_ids = list(set(user_ids).difference([restaurant_rating[4] for restaurant_rating in restaurant_rating_data]))
            if not available_user_ids:
                log.error('There are no available users to be added to restaurant ratings')
                raise Exception('There are no available users to be added to restaurant ratings')
            user_id = random.choice(available_user_ids)
        else:
            user_id = random.choice(user_ids)
    else:
        log.error('There are no available users to be added to restaurant ratings')
        raise Exception('There are no available users to be added to restaurant ratings')
    return user_id

def generate_rating():
    id = int(fake.numerify(text='###########'))
    imageId = fake.uuid4()
    stars = random.randrange(0,5)
    description = fake.paragraph()
    user = get_user_id()
    return Rating(id, imageId, stars, description, user)

def generate_hours():
    return Hours([random.choice(hour_options) for i in range(7)])

def generate_restaurant():
    id = int(fake.numerify(text='###########'))
    averageRating = 5
    averageTime = random.randrange(0,30)
    backgroundId = fake.uuid4()
    geolocation = fake.local_latlng(country_code='US')
    address = fake.street_address() + '\n' + geolocation[2] + ', ' + geolocation[3]
    hours = generate_hours().toDict()
    iconId = fake.uuid4()
    name = random.choice(restaurant_names)
    ratings = generate_rating().stars
    return Restaurant(id, address, averageRating, averageTime, backgroundId, 
                 geolocation, hours, iconId, name, ratings)

def addMenuToDb():
    menu = generate_menu().toDict()
    log.info(menu)
    prepare_statement(CrudOperation.CREATE, 'menu_item_entity', config=global_config, **menu)

def addPromotionToDb():
    promotion = generate_promotions().toDict()
    log.info(promotion)
    prepare_statement(CrudOperation.CREATE, 'promotions_entity', config=global_config, **promotion)

def addRatingToDb():
    rating = generate_rating().toDict()
    log.info(rating)
    prepare_statement(CrudOperation.CREATE, 'restaurant_rating_entity', config=global_config, **rating)

def addRestaurantToDb():
    # select * from rating and get the average
    restaurant = generate_restaurant().toDict()
    log.info(restaurant)
    prepare_statement(CrudOperation.CREATE, 'restaurant_entity', config=global_config, **restaurant)

# gets a random restaurant id, and a random feature (menu, promotion, ratings) id
def get_restaurant_feature_id(table):
    restaurant_data = prepare_statement(CrudOperation.READ, 'restaurant_entity', config=global_config)
    feature_data = prepare_statement(CrudOperation.READ, table, config=global_config)
    feature_id = ''
    restaurant_id = ''

    # if theres any data in the feature, give a random feature to a random restaurant
    if feature_data:
        feature_ids = [feature[0] for feature in feature_data]
        if not feature_ids:
            log.error('There is no data to be added!')
            raise Exception('There is no data to be added!')
        feature_id = random.choice(feature_ids)
    else:
        log.error('There is no restaurant feature data to be added!')
        raise Exception('There is no restaurant feature data to be added!')
    
    if restaurant_data:
        restaurant_ids = [restaurant[0] for restaurant in restaurant_data]
        if not restaurant_ids:
            log.error('There are no restaurants to be added!')
            raise Exception('There are no restaurants to be added!')
        restaurant_id = random.choice(restaurant_ids)
    else:
        log.error('There are no restaurants to be added!')
        raise Exception('There are no restaurants to be added!')
    
    return (restaurant_id, feature_id)

# add menu id and restaurant id to restaurant_entity_menu table
def addMenuToRestaurantDb():
    id = get_restaurant_feature_id('menu_item_entity')
    restaurant_menu = {'restaurant_entity_id': id[0], 'menu_id': id[1]}
    log.info(restaurant_menu)
    prepare_statement(CrudOperation.CREATE, 'restaurant_entity_menu', config=global_config, **restaurant_menu)

# add promotions id and restaurant id to restaurant_entity_promotions table
def addPromotionToRestaurantDb():
    id = get_restaurant_feature_id('promotions_entity')
    restaurant_promotion = {'restaurant_entity_id': id[0], 'promotions_id': id[1]}
    log.info(restaurant_promotion)
    prepare_statement(CrudOperation.CREATE, 'restaurant_entity_promotions', config=global_config, **restaurant_promotion)

# add menu id and restaurant id to restaurant_entity_menu table
def addRatingToRestaurantDb():
    id = get_restaurant_feature_id('restaurant_rating_entity')
    restaurant_rating = {'restaurant_entity_id': id[0], 'ratings_id': id[1]}
    log.info(restaurant_rating)
    prepare_statement(CrudOperation.CREATE, 'restaurant_entity_ratings', config=global_config, **restaurant_rating)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    addMenuToRestaurantDb()