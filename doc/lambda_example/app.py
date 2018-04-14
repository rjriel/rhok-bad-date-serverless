import os
#libs for working with AWS
import boto3
import botocore

import uuid
import re
from hashlib import md5


sd = boto3.resource('s3')
regex = os.environ['FILE_REGEX']

#the entry point for hte lambda function
def lambda_handler(event, context):
    s3_key = None
    try:
        s3 = boto3.resource('s3')
        s3_key = event['Records'][0]['s3']['object']['key']
        bucket_name =  event['Records'][0]['s3']['bucket']['name'].translate({ord(c):'+' for c in '-:'})
        if not re.match(regex, bucket_name):
            return {'message' : 'Object did not pass filter, not hasing'}
        bucket = s3.Bucket(bucket_name)
        path = pull_file(s3_key, bucket)
        file_hash = hash_file(path)
        if not file_hash:
            raise
        if not insert_hash(file_hash, s3_key, bucket_name):
            raise
    except Exception as e:
        print('Error while hashing file, and inserting to DynamoDB')
        print(e)
        return {'message' : 'Uanble to has and insert {}/{} to database'.format(bucket_name, s3_key)}

    return {'message' : '{} hashed and inserted to database'.format(s3_key)}

def pull_file(resource_key, bucket):
    loc = uuid.uuid4()
    path = '/tmp/{}'.format(loc)
    try:
        s3_object = bucket.download_file(resource_key, path)

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] is '404':
            print('The object at {} does not exist'.format(resource_key))
        else:
            print('Error while retreiving object')
        return None

    return path

def hash_file(path):
    file_to_hash = None
    md5_hash = md5()

    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
    except Exception as e:
        print('Exception while opening and hasing file at {}'.format(path))
        return None 
    
    return md5_hash.hexdigest()

def insert_hash(file_hash, s3_key, bucket_name):
    try:
        #the cloudformation will define environment variables to get system information from
        #for example the name of the table
        table_name = os.environ['HASH_TABLE']
        region = os.environ['AWS_REGION']
        primary_key = os.environ['TABLE_PARTITION_KEY']

        db = boto3.resource('dynamodb', region_name=region)
        table = db.Table(table_name)
        # make primary key bucket_name/object_id
        hash_details = {'hash' : file_hash, primary_key : '{}/{}'.format(bucket_name,s3_key)}

        result = table.put_item(TableName=table_name, Item=hash_details)
        
        return result['ResponseMetadata']['HTTPStatusCode']

    except Exception as e:
        print('Error while inserting hash to database : {}'.format(e))
        return None
    
