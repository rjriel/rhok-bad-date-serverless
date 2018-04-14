#/usr/bin/python3

import boto3
import hashlib
import os

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.digest()

def insert_user():
  pass

def check_user(client, username):
    response = client.get_item(TableName='user',
        Key={'username' : {'S': username}})
    
    print(response)

  
def lambda_handler(event, ctx):
  #gross, find a way to not hard code that 
  dynamo_client = boto3.client('dynamodb')
  check_user(dynamo_client, 'test')

