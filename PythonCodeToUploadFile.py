import boto3
import boto.s3
import sys
from boto.s3.key import Key

s3 = boto3.resource('s3')

local_data_path = sys.argv[1]
local_query_path = sys.argv[2]
bucket_name = sys.argv[3]
s3_file_location = sys.argv[4]

s3.meta.client.upload_file(local_data_path, bucket_name, s3_file_location + '/data.csv')
s3.meta.client.upload_file(local_query_path, bucket_name, s3_file_location + '/query.txt')
