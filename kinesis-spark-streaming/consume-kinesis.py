from boto import kinesis
import time

kinesis = kinesis.connect_to_region("us-east-1")
print(kinesis.list_streams())
shard_id = 'shardId-000000000000' #we only have one shard!
shard_it = kinesis.get_shard_iterator("qqd-data-stream", shard_id, "LATEST")["ShardIterator"]

while 1==1:
  out = kinesis.get_records(shard_it, limit=1)
  print(out["Records"])
  shard_it = out["NextShardIterator"]
  if len(out["Records"])>0:
    print(out["Records"][0]["Data"])
  else:
    print('records are empty')
  time.sleep(0.3)