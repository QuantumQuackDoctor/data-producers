import json, string, time
from boto3 import resource
from random import seed, randint, choice

seed(1)
food_list = ["Rice","Beans","Eggs","Chicken","Lamb"]
price_list = [20.00, 15.00, 5.65,9.99,15.99]

bucket_name = 'qqd-producer-output'
s3 = resource('s3')

# generate 6 character alphanumeric id
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(choice(chars) for _ in range(size))

# generate order
def generateOrder():
	id = id_generator()
	i = randint(0,len(food_list)-1)
	data = {'id': id, 'food': food_list[i], 'price': price_list[i]}

	response = s3.Object(bucket_name, str(id)+'.json').put(Body=json.dumps(data, indent=2).encode('utf-8'))
	print(response)
	time.sleep(1)
	
	# with open('output-data/'+str(id)+'.json', "w") as writeJSON:
	# 	json.dump(data, writeJSON)

while True:
	generateOrder()
	time.sleep(0.2)

