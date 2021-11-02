import psycopg2, time
from config import *

log = logging.getLogger(__name__)
db_config = config()

def create_schema():
    '''runs dbschema.sql to create all tables'''
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        if conn != None:
            log.info('Database is Connected!')
    except psycopg2.OperationalError:
        log.error('Database is not online, time limit reached!')

    cur = conn.cursor()
    with open(ROOT_DIR + '/db/dbschema.sql', 'r') as sql_file:
        cur.execute(sql_file.read())
    log.info(cur.fetchall())
    log.info('Tables created!')

    conn.commit()
    conn.close()
    return conn
    
def truncate_db():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    log.info('Deleting Contents of user_entity...')
    cur.execute('TRUNCATE user_entity CASCADE;')
    conn.commit()
    conn.close()
    log.info('Done!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    create_schema()
    # tearDown()

