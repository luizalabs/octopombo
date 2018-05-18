import json
import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

from octopombo.common.exceptions import HttpError

logger = logging.getLogger(__name__)


class S3Manager:

    _instance = None

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.client = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME

    def upload(self, data, filename):
        s3_object = self.client.Object(self.bucket, filename)

        logger.info(
            'upload file {} to s3 bucket {}'.format(filename, self.bucket)
        )
        try:
            s3_object.put(
                Body=json.dumps(data),
                ContentType='application/json',
                ACL='public-read'
            )

        except ClientError as e:
            logger.error('Fail to update file {}, error: {}'.format(
                filename, e.response
            ))
            raise HttpError(message=e.response['Error']['Code'])

    def delete(self, filename):
        s3_object = self.client.Object(self.bucket, filename)

        logger.info('Delete file {} from s3 bucket {}'.format(
            filename, self.bucket
        ))
        try:
            s3_object.delete()
        except ClientError as e:
            logger.error('Fail to delete file {} of s3 bucket {}'.format(
                filename, self.bucket
            ))
            raise HttpError(message=e.response['Error']['Code'])

    def get(self, filename):
        s3_bucket = self.client.Bucket(self.bucket).meta.client
        try:
            s3_bucket.download_file(
                Bucket=self.bucket,
                Key=filename,
                Filename=filename
            )
            with open(filename) as json_file:
                data = json.load(json_file)

            return data
        except ClientError as e:
            logger.error(
                'Fail to get files on s3 bucket '
                '{bucket} error {error}'.format(
                    bucket=self.bucket,
                    error=e
                )
            )
            raise HttpError(message=e.response['Error']['Code'])
