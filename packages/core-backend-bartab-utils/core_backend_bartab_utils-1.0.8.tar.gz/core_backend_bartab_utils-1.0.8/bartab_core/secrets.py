import boto3
import base64
from botocore.exceptions import ClientError
from django.conf import settings


def get_secret(secret_name: str, region_name: str=None):
    if region_name == None:
        region_name = settings.DEFAULT_AWS_SECRET_REGION

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(
                get_secret_value_response['SecretBinary'])
