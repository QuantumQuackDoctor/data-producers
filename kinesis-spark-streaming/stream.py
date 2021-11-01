from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
from pyspark.sql.types import *

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages=org.apache.spark:spark-streaming-kinesis-asl_2.12:3.1.2'

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[*]", "qqd-data-stream")
ssc = StreamingContext(sc, 1)

kinesisStream = KinesisUtils.createStream(
    ssc, 'qqd-data-stream', 'qqd-data-stream', 'https://kinesis.us-east-1.amazonaws.com', 'us-east-1', InitialPositionInStream.TRIM_HORIZON, 2
)
# print(kinesisStream.)
kinesisStream.pprint()
outputBuffer = []

def get_output(streamRDD):
	print(streamRDD)
	print(streamRDD.collect())

	# for e in rdd.collect():
	# 	print('---',e)
	# 	outputBuffer.append(e)
kinesisStream.foreachRDD(get_output)

counts = kinesisStream.map(lambda line: print(type(line)))


# Start the context
ssc.start()
ssc.awaitTermination()
# spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.12:3.1.2 stream.py