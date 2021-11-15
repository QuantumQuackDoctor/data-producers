import unittest
from config import config
from generate_orders import *
from dao import *

class UserTest(unittest.TestCase):

    def setUp(self):
        # change config to test config
        self.params = config(section='h2')

        # test connection
        self.conn = psycopg2.connect(**self.params)
        self.assertIsNotNone(self.conn)

        # test table
        cur = self.conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('food_order_entity')))
        self.assertIsNotNone(cur.fetchall())

    # test get id function
    def test_get_ids(self):
        ids = get_ids()
        self.assertIsNotNone(ids)

    # test generate_order function
    def test_generate_order(self):
        food_order = generate_order()
        self.assertIsNotNone(food_order)

    def test_read(self):
        cur = self.conn.cursor()
        self.assertIsNotNone(self.conn)

        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('order_entity')))
        expected = cur.fetchall()

        actual = prepare_statement(CrudOperation.READ, 'order_entity', self.params)
        self.assertEqual(expected, actual)
    
    # test add_food_order_to_db function
    def test_add_order_to_db(self):
        expected_order_entity = prepare_statement(CrudOperation.READ, 'order_entity', self.params)
        expected_food_order_entity = prepare_statement(CrudOperation.READ, 'food_order_entity', self.params)
        expected_food_order_entity_order_items = prepare_statement(CrudOperation.READ, 'food_order_entity_order_items', self.params)
        expected_order_entity_items = prepare_statement(CrudOperation.READ, 'order_entity_items', self.params)
        expected_user_entity_order_list = prepare_statement(CrudOperation.READ, 'user_entity_order_list', self.params)

        add_order_to_db()

        actual_order_entity = prepare_statement(CrudOperation.READ, 'order_entity', self.params)
        actual_food_order_entity = prepare_statement(CrudOperation.READ, 'food_order_entity', self.params)
        actual_food_order_entity_order_items = prepare_statement(CrudOperation.READ, 'food_order_entity_order_items', self.params)
        actual_order_entity_items = prepare_statement(CrudOperation.READ, 'order_entity_items', self.params)
        actual_user_entity_order_list = prepare_statement(CrudOperation.READ, 'user_entity_order_list', self.params)

        self.assertEqual(len(expected_order_entity)+1, len(actual_order_entity))
        self.assertEqual(len(expected_food_order_entity)+1, len(actual_food_order_entity))
        self.assertEqual(len(expected_food_order_entity_order_items)+1, len(actual_food_order_entity_order_items))
        self.assertEqual(len(expected_order_entity_items)+1, len(actual_order_entity_items))
        self.assertEqual(len(expected_user_entity_order_list)+1, len(actual_user_entity_order_list))

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    unittest.main()
