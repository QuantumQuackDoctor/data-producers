# Setup

## Running on local
### Install required packages
```
pip install -r requirements.txt
```
### Secrets Setup AWS Credentials for Database Secrets
First install [`aws-cli`](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)  and then
```
aws configure
```

### Change [section] in for each producer if needed (look at line 22 of config.py if you're getting errors and change as needed)

## Running on AWS Cloud
``` 
aws cloudformation deploy --stack-name Data-${params.Environment} --region ${AWS_REGION} --template-file data-producer-cf.yaml  --parameter-overrides Environment=${params.Environment} KeyName=${KeyName} --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM
```

## Running on Jenkins and AWS Cloud
You can setup Jenkins to pull from this repo and the pipeline would do the rest

## pgadmin
The cloudformation template sets up a docker instance for pgadmin. To access this:
```
<ipv4>:5050
username: admin@admin.com
password: root
```
To see your database secrets actual value, connect to the ec2 instance
```
cd data-producers
python3 db/config.py
```
Use that to create a server on pgadmin