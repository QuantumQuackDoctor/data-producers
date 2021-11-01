import logging
from configparser import ConfigParser
from pathlib import Path

ROOT_DIR = str(Path(__file__).parent.resolve().parents[0])
log = logging.getLogger(__name__)

def config(filename=ROOT_DIR+'/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    db = {}

    try:
        # read config file
        with open(filename, 'r') as file:
            parser.read_file(file)
            # get section, default to postgresql
            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    db[param[0]] = param[1]
            else:
                raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    except FileNotFoundError as e:
        print(e)

    return db