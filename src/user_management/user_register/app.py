#/usr/bin/python3

import boto3
import hashlib
from uuid import uuid4
import os

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  return passwd_hash.digest()

def create_user(client, event):
  passwd = hash_passwd(event['password'])
  table = client.table('user')
  table.put_item(Item={'username' : {'S' : event['username']},
                      {'S' : 'password' : passwd}})
  

def user_exists(client, username):
    response = client.get_item(TableName='user',
        Key={'username' : {'S': username}})
    
    if not response:
      #the user does not exist
      return False
    else:
      #the User does exist
      return True

  
def lambda_handler(event, ctx):
  #gross, find a way to not hard code that 
  dynamo_client = boto3.client('dynamodb')
  if not  check_user(dynamo_client, event['username']):
    create_user(event)
  else:
    return [False, "Username already exists"]

