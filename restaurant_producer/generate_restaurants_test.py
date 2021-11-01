import unittest
from config import config
from generate_restaurants import *
from dao import *

class RestaurantTest(unittest.TestCase):
    
    def setUp(self):
        # change config to test config
        self.params = config(section='h2')

        # test connection
        self.conn = psycopg2.connect(**self.params)
        self.assertIsNotNone(self.conn)

        # test schema by checking number of tables in db
        cur = self.conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('restaurant_entity')))
        self.assertIsNotNone(cur.fetchall())

    # test generate_restaurant function
    def test_generate_restaurant(self):
        restaurant = generate_restaurant()
        self.assertIsNotNone(restaurant)
    
    # test generate_menu function
    def test_generate_menu(self):
        menu = generate_menu()
        self.assertIsNotNone(menu)
    
    # test generate_promotions function
    def test_generate_promotions(self):
        promotions = generate_promotions()
        self.assertIsNotNone(promotions)
    
    # test get_user_id function
    def test_get_user_id(self):
        ids = get_user_id()
        self.assertIsNotNone(ids)
    
    # test generate_rating function
    def test_generate_rating(self):
        rating = generate_rating()
        self.assertIsNotNone(rating)
    
    # test generate_hours function
    def test_generate_hours(self):
        hours = generate_hours()
        self.assertIsNotNone(hours)
    
    # test get_restaurant_feature_id function
    def test_restaurant_feature_id(self):
        feature = get_restaurant_feature_id('menu_item_entity')
        self.assertIsNotNone(feature)
    
    def test_read(self):
        cur = self.conn.cursor()
        self.assertIsNotNone(self.conn)

        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('restaurant_entity')))
        expected = cur.fetchall()

        actual = prepare_statement(CrudOperation.READ, 'restaurant_entity', self.params)
        self.assertEqual(expected, actual)

    # test addRestaurantToDb function
    def test_add_restaurant_to_db(self):
        expected = prepare_statement(CrudOperation.READ, 'restaurant_entity', self.params)
        addRestaurantToDb()
        actual = prepare_statement(CrudOperation.READ, 'restaurant_entity', self.params)
        self.assertEqual(len(expected)+1, len(actual))

    # test addMenuToDb function
    def test_add_menu_to_db(self):
        expected = prepare_statement(CrudOperation.READ, 'menu_item_entity', self.params)
        addMenuToDb()
        actual = prepare_statement(CrudOperation.READ, 'menu_item_entity', self.params)
        self.assertEqual(len(expected)+1, len(actual))

    # test addPromotionToDb function
    def test_add_promotion_to_db(self):
        expected = prepare_statement(CrudOperation.READ, 'promotions_entity', self.params)
        addPromotionToDb()
        actual = prepare_statement(CrudOperation.READ, 'promotions_entity', self.params)
        self.assertEqual(len(expected)+1, len(actual))

    # test addRatingToDb function
    def test_add_rating_to_db(self):
        expected = prepare_statement(CrudOperation.READ, 'restaurant_rating_entity', self.params)
        addRatingToDb()
        actual = prepare_statement(CrudOperation.READ, 'restaurant_rating_entity', self.params)
        self.assertEqual(len(expected)+1, len(actual))

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    unittest.main()
