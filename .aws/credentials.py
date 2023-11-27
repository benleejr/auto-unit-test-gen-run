import os
import boto3
import pandas
from dotenv import load_dotenv

load_dotenv('.env')

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = S3_ACCESS_KEY,
    aws_secret_access_key = S3_SECRET_ACCESS_KEY,
    region_name = 'us-east-2'
)
    
# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = S3_ACCESS_KEY,
    aws_secret_access_key = S3_SECRET_ACCESS_KEY,
    region_name = 'us-east-2'
)

# Fetch the list of existing buckets
clientResponse = client.list_buckets()
    
# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')