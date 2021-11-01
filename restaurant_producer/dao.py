import enum, traceback, psycopg2, logging
from config import config
from psycopg2 import sql

log = logging.getLogger(__name__)

class CrudOperation(enum.Enum):
    CREATE = 'insert'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'

def run_statement(config, query, *args):
    
    conn = None
    data = None
    try:
        # connect to the PostgreSQL server and execute statement
        log.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**config)
        
        # execute statement(s)
        cur = conn.cursor()
        cur.execute(query, args)
        if 'SELECT' in query.as_string(conn):
            data = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except psycopg2.Error as error:
        log.error('[%s %s]'%error.diag.severity, error.diag.message_primary)
        traceback.log.debug_exc()
    finally:
        if conn is not None:
            conn.close()
            log.debug("PostgreSQL connection is closed")
        return data

def prepare_statement(crud, table, config=config(), **kwargs):

    if not isinstance(crud, CrudOperation):
        raise TypeError('crud must be an instance of CrudOperation Enum')

    if crud == CrudOperation.CREATE:
        keys = list(kwargs)
        values = tuple(kwargs.values())
        statement = ''' INSERT INTO {table} ({}) VALUES %s;'''
        query = sql.SQL(statement).format(sql.SQL(', ').join(map(sql.Identifier, keys)),table=sql.Identifier(table))
        log.debug('Adding to db...')
        return run_statement(config, query, values)
    elif crud == CrudOperation.READ:
        statement = ''' SELECT * FROM {table}'''
        query = sql.SQL(statement).format(table=sql.Identifier(table))
        log.debug('Reading from db...')
        return (run_statement(config, query, (table)))
    elif crud == CrudOperation.UPDATE:
        pass
    elif crud == CrudOperation.DELETE:
        statement = ''' DELETE FROM {table} WHERE {} = {} RETURNING (select_list | *)'''
        query = sql.SQL(statement).format(table=sql.Identifier(table))
        return (run_statement(config, query, (table)))

if __name__ == '__main__':
    prepare_statement(CrudOperation.READ, 'restaurant_entity')