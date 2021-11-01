import psycopg2, time, docker
from config import config, ROOT_DIR

container_config = config(section='dbcontainer')
db_config = config(section='postgresql')
client = docker.from_env()

def set_up_docker_db():
    '''starts a new postgres docker container'''
  
    print('[INFO] Attempting to start docker container...')
    try:
        if client.images.get(container_config['image']):
            client.containers.run(
                container_config['image'],
                ports={container_config['ports'].split(':')[0]: container_config['ports'].split(':')[1]},
                detach=True,
                name=container_config['name'],
                environment=["POSTGRES_PASSWORD=%s"%container_config['password']],
            )
        print('[INFO] Docker container',container_config['name'], 'started!')
    except docker.errors.ImageNotFound:
        print('[ERROR]', container_config['image'], 'image does not exist locally!')
        try:
            print('[INFO] pulling', container_config['name'], '...')
            client.images.pull(container_config['image'])
            print('[INFO] Restart the setup')
        except docker.errors.APIError:
            print('[ERROR] problem pulling', container_config['image'],', check if the image is correct!')
    except docker.errors.APIError:
        print('[INFO]', container_config['name'], 'is already running.')

def create_schema():
    '''runs dbschema.sql to create all tables'''
    set_up_docker_db()
    conn = None
    con_tries = 4
    while conn == None and con_tries >= 0:
        try:
            conn = psycopg2.connect(**db_config)
            if conn != None:
                print('[INFO] Database is Connected!')
                break
        except psycopg2.OperationalError:
            time.sleep(1.2)
            con_tries -= 1
            if con_tries < 0:
                print('[Error] Database is not online, time limit reached!')
            else:
                print('[WARN] Database is not online, Reattempting to connect',con_tries)

    cur = conn.cursor()
    with open(ROOT_DIR + '/db/dbschema.sql', 'r') as sql_file:
        cur.execute(sql_file.read())
    print('[INFO]', cur.fetchall())
    print('[INFO] Tables created!')

    conn.commit()
    conn.close()
    return conn
    
def truncate_db():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    print('[INFO] Deleting Contents of user_entity...')
    cur.execute('TRUNCATE user_entity CASCADE;')
    conn.commit()
    conn.close()
    print('[INFO] Done!')

def tear_down_container():
    try:
        container = client.containers.get(container_config['name'])
        print('[INFO] stopping', container_config['name'], '...')
        container.stop()
        print('[INFO] removing', container_config['name'], '...')
        container.remove()
    except docker.errors.APIError:
        print('[ERROR] problem with', container_config['image'])

if __name__ == '__main__':
    create_schema()
    # tearDown()

