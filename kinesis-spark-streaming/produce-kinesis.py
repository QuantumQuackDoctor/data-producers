import json
from boto import kinesis
import sys

from random import seed
from random import randint
import time
import random

kinesis = kinesis.connect_to_region("us-east-1")
print(kinesis.list_streams())

seed(1)
i = 0
while 1 == 1:
	data = "Hello "+ str(i)
	# data["timestamp"] = int(time.time())
	# data["dataNum"] = "data"+str(i)
	# data["device_name"] = "dev"
	# data["HeartRate"] = random.randint(60, 120)
	

	print("uploading ", data)
	kinesis.put_record("qqd-data-stream", data, "partitionkey")
	time.sleep(0.2)
	i += 1
