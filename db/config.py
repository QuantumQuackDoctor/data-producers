import boto3
from configparser import ConfigParser
from pathlib import Path
from botocore.exceptions import ClientError

ROOT_DIR = str(Path(__file__).parent.resolve().parents[0])
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name='us-east-1',
)
def config(filename=ROOT_DIR+'/database.ini', section='postgresql_test'):
    parser = ConfigParser()
    db = {}
    
    with open(filename, 'r') as file:
        parser.read_file(file)
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_project_root() -> Path:
  """Returns project root folder."""
  return str(Path(__file__).parents[1])


def get_secret(secret_name):

    text_secret_data = ''

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
    
    return text_secret_data

print(get_secret('UserTGArn-prod'))

