import json
import boto3
import streamlit as st

# set up credentials and endpoint names
# with open('aws_access_key.json', 'r') as f:
#     credentials = json.load(f)

aws_access_key_id = st.secrets['aws_access_key_id']
aws_secret_access_key = st.secrets['aws_secret_access_key']

# s3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

s3_bucket_name = "sentiment-results-bucket"
s3_bucket = boto3.resource('s3').Bucket(s3_bucket_name)

# lambda client
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='ap-southeast-1'
)

lambda_function_name = "wogaa-sentiments-predict"
