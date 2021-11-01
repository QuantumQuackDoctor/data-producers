# Setup

## Install required packages
```
pip install -r requirements.txt
```

## Setup AWS Credentials
First install [`aws-cli`](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)  and then
```
aws configure
```

### create your own database.ini file with the format below
```
[postgresql]
host=10.0.2.15
database=postgres
user=postgres
password=password
port=5432
[dbcontainer]
image=postgres:latest
ports=5432:5432
name=postgres-qqd-database
password=password
[h2]
dbname=test-db
user=test
password=password
host=localhost
port=5435
```