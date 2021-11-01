import unittest, logging
from config import config
from generate_driver import *
from dao import *

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class UserTest(unittest.TestCase):
        
    def setUp(self):
        # change config to test config
        self.params = config(section='h2')

        # test connection
        self.conn = psycopg2.connect(**self.params)
        self.assertIsNotNone(self.conn)

        # test schema by checking number of tables in db
        cur = self.conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('driver_entity')))
        self.assertIsNotNone(cur.fetchall())

    # test generate_driver function
    def test_generate_driver(self):
        driver = generate_driver()
        self.assertIsNotNone(driver)

    # test generate_driver_ratings function
    def generate_driver_ratings(self):
        driver_rating = generate_driver_ratings()
        self.assertIsNotNone(driver_rating)

    # test CrudOperation.READ read
    def test_read(self):
        cur = self.conn.cursor()
        self.assertIsNotNone(self.conn)

        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('driver_entity')))
        expected = cur.fetchall()

        actual = prepare_statement(CrudOperation.READ, 'driver_entity', self.params)
        self.assertEqual(expected, actual)
    
    # test add_driver_to_db function
    def test_add_driver_to_db(self):
        driver = generate_driver()
        expected = prepare_statement(CrudOperation.READ, 'driver_entity', self.params)
        prepare_statement(CrudOperation.CREATE, 'driver_entity', self.params, **driver.toDict())
        actual = prepare_statement(CrudOperation.READ, 'driver_entity', self.params)
        
        self.assertEqual(len(expected)+1, len(actual))

    # test add_driver_ratings_to_db function
    def test_add_driver_ratings_to_db(self):

        driver = generate_driver_ratings()

        expected = prepare_statement(CrudOperation.READ, 'driver_rating_entity', self.params)
        prepare_statement(CrudOperation.CREATE, 'driver_rating_entity', self.params, **driver.toDict())
        actual = prepare_statement(CrudOperation.READ, 'driver_rating_entity', self.params)
        
        self.assertEqual(len(expected)+1, len(actual))

if __name__ == '__main__':
    unittest.main()
