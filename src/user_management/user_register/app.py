#/usr/bin/python3

import boto3
import boto-core
import os


def lambda_handler(event, ctx):
  iam = boto3.connect()
