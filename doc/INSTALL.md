# Installation

## IAM

A Iam role is required for the app to run, and should be authorized for the api gateway, dynamoDB, and Lambda

The roll must be named bad-date, and implement the following Policies

AWSLambdaFullAccess - This is a default policy offered by AWS

A policy called "gateway-policy", it's description is as follows

`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "apigateway:*",
            "Resource": "*"
        }
    ]
}`

A policy called "lambda_dynamo_reading", it's description is as follows

`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeReservedCapacityOfferings",
                "dynamodb:TagResource",
                "dynamodb:UntagResource",
                "dynamodb:ListTables",
                "dynamodb:DescribeReservedCapacity",
                "dynamodb:ListBackups",
                "dynamodb:PurchaseReservedCapacityOfferings",
                "dynamodb:ListTagsOfResource",
                "dynamodb:DescribeTimeToLive",
                "dynamodb:DescribeLimits",
                "dynamodb:ListStreams"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "arn:aws:dynamodb:*:*:table/*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "arn:aws:dynamodb:*:*:table/*/index/*"
        }
    ]
}`


This role should have the identity providers apigateway.amazonaws.com and lambda.amazonaws.com set as trusted  entities

## Database

Three dynamodb tables are needed

### incident_report

* Table Name: incident_report

* Primary Key :  incident_id(String)

### token

* Table Name: token

* Primary Key: user_name(String)

* ttl column: ttl(Number)

### user

* Table Name: user

* Primary Key: user_name

## Lambda Functions

Lambda functions are found under the src directory of this repository, and can be installed with the lambda console, they will require the following configurations

### User Register

* name: user_register

* runtime: Python3.6

* source: $REPO_ROOT/src/user_management/user_register/app.py

* Environment Variables: DEBUG=0

### User Login

* name: user_login

* runtime: Python3.6

* source: $REPO_ROOT/src/user_management/user_login/app.py

* environment variables: DEBUG=0 , MINUTES_TO_LIVE=60

### Incident Create

* name: incident_create

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/incident_create/app.py

* environment variables: 

### Incident Retrieve

* name: incident_retrieve

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/incident__retrieve/app.py

* environment variables: 

### Incident Add Comment

* name: incident_add_comment

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/incident_add_comment/app.py

* environment variables: 

### Incident Delete

* name: incident_delete

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/incident_delete/app.py

* environment variables: 

### Anonymous Incident Retrieve

* name: anonymous_incident_retrieve

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/anonymous_incident_retrieve/app.py

* environment variables: 

### Incident Update

* name: incident_update

* runtime: Python3.6

* source: $REPO_ROOT/src/base_crud/incident_update/app.py

* environment variables: 

### Requestion Autohrizor

* name: request_authorizer

* runtime: Python3.6

* source: $REPO_ROOT/src/gateway_auth/session_authorizer/app.py

* environment variables: DEBUG=1

## API Gateway

The API gateway used for this app is described with the swagger documentation and code provided in the repo, please refer to that for deploying the API Gateway API endpoints for the bad-date app.

Documentation about this API implmentation can be found in the $REPO_ROOT/doc directory

### Authorizers

#### request-authorizer

* Lambad Function: request_authorizer

* Lambad Event Payload: Request

* Authroization Caching: 0 (Not enabled)

* Identity Sources:

  * Query String : username
  
	* Query String : authorization


### Authroized API's

All '/incident' API endpoints need to implement the request-authorizer at the Method REquest step. 
