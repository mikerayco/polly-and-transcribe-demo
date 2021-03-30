import re

import boto3


def upload_file(file_path, bucket):
    client = boto3.client('s3')
    file_name = re.findall("([^\/]+$)", file_path)[0]
    response = client.upload_file(file_path, bucket, file_name)
    return response
