#/usr/bin/python3

import boto3
import hashlib
from uuid import uuid4
import os

def hash_password(passwd):
  passwd_hash = hashlib.sha256()
  passwd_hash.update(passwd.encode('utf-8'))
  if os.getenv('DEBUG') is '1':
    print('password hash is {}'.format(passwd_hash.hexdigest))
  return passwd_hash.hexdigest()

def create_user(client, event):
  passwd = hash_password(event['password'])
  client.put_item(TableName='user', Item={'user_name' : {'S' : event['name']},
                      'password' : {'S' : passwd},
                      'role' : {'S' : 'submitter'}
  })
  

def user_exists(client, username):
    response = client.get_item(TableName='user',
        Key={'user_name' : {'S': username}})
    if os.getenv('DEBUG') is '1':
      print('dynamo response is \n {}'.format(response))
    if not 'Item' in response:
      #the user does not exist
      return False
    else:
      #the User does exist
      return True

  
def lambda_handler(event, ctx):
  debug = os.getenv('DEBUG') is '1'
  if debug:
    print('EVENT*******')
    print(event)
  dynamo_client = boto3.client('dynamodb')
  if not  user_exists(dynamo_client, event['name']):
    if debug:
      print('creating user {}'.format(event['name']))
    create_user(dynamo_client, event)
    return { 'success': True }
  else:
    return { 'success': False, 'message': "Username already exists" }


if __name__ == '__main__':
  os.environ['DEBUG'] = '1'
  lambda_handler({'name' : str(uuid4()), 'password' : 'password1234'}, {})
