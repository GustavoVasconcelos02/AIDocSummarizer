from dotenv import load_dotenv
import boto3
import os

# Carregar o arquivo .env
load_dotenv()

# Cliente AWS e credenciais
def get_bedrock_client():
    client = boto3.client(
        'bedrock',
        region_name='us-east-1',
        endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )
    return client