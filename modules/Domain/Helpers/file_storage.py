import os
import logging
from typing import List, Optional

import boto3
from botocore.exceptions import ClientError, ConnectionError
from botocore.config import Config

EXPIRATION_SEC = 60
S3 = boto3.client(
        's3',
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'}
        )
    )



def _s3_error_handler(func):
    def wrapper(*args):
        try:
            func(*args)
        except ClientError as e:
            logging.error(f"Service failed: {e.response['Error']['Message']}")
            raise Exception("Service failed")
        except ConnectionError as e:
            logging.error(f"Service unavailable: {e}")
            raise Exception("Service unavailable")
        return func(*args)
    return wrapper


@_s3_error_handler
def get_upload_url(
        bucket_name: str, object_name: str, fields: dict = None,
        conditions: List[str] = None, expiration: int = EXPIRATION_SEC
) -> Optional[dict]:
    """Generate a presigned URL S3 POST request to upload a file"""
    response = S3.generate_presigned_post(
        bucket_name,
        object_name,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=expiration
    )
    return response


@_s3_error_handler
def get_download_url(bucket_name: str, object_name: str,
                     expiration: int = EXPIRATION_SEC) -> Optional[str]:
    """Generate a presigned URL to download an S3 object"""
    response = S3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration
    )
    return response


@_s3_error_handler
def get_files_by_id(bucket_name: str, borrower_id: str) -> Optional[List]:
    response = S3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=borrower_id
    )
    return response.get('Contents')


@_s3_error_handler
def delete_file(bucket_name: str, object_name: str) -> Optional[dict]:
    response = S3.delete_object(
        Bucket=bucket_name,
        Key=object_name
    )
    return response


@_s3_error_handler
def upload_file(file, bucket_name, object_name):
    try:
        _ = S3.upload_file(file, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
