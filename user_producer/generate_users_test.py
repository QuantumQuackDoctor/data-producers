import unittest
from config import config
from generate_users import *
from dao import *

class UserTest(unittest.TestCase):
        
    def setUp(self):
        # change config to test config
        self.params = config(section='h2')

        # test connection
        self.conn = psycopg2.connect(**self.params)
        self.assertIsNotNone(self.conn)

        # test schema by checking number of tables in db
        cur = self.conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('user_entity')))
        self.assertIsNotNone(cur.fetchall())

    # test generate_user function
    def test_generate_user(self):
        user = generate_user()
        self.assertIsNotNone(user)
    
    # test add_user_to_db function
    def test_add_user_to_db(self):
        expected = prepare_statement(CrudOperation.READ, 'user_entity', self.params)
        add_user_to_db()
        actual = prepare_statement(CrudOperation.READ, 'user_entity', self.params)
        self.assertEqual(len(expected)+1, len(actual))

    def test_read(self):
        cur = self.conn.cursor()
        self.assertIsNotNone(self.conn)

        cur.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('user_entity')))
        expected = cur.fetchall()

        actual = prepare_statement(CrudOperation.READ, 'user_entity', self.params)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    unittest.main()
