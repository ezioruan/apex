import boto3
from botocore.exceptions import ClientError

from apex_fastapi.constants import S3ACL


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def generate_presigned_post(
        self,
        bucket_name,
        object_name,
        fields=None,
        conditions=None,
        expiration=3600,
        acl=S3ACL.PUBLIC_READ_WRITE.value,
    ):
        try:
            if not fields:
                fields = {}
            fields["acl"] = acl
            conditions = (
                conditions.append({"acl": acl})
                if conditions
                else [{"acl": acl}]
            )
            response = self.client.generate_presigned_post(
                bucket_name,
                object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError:
            print(
                "Couldn't get a presigned post for client method.",
            )
            raise ClientError
        return response

    def generate_presigned_url(
        self, client_method, method_parameters, expires_in, acl=S3ACL.PRIVATE
    ):
        """
        Generate a presigned Amazon S3 URL that
            can be used to perform an action.

        :param s3_client: A Boto3 Amazon S3 client.
        :param client_method: The name of the client
            method that the URL performs, for example, 'put_object'.
        :param method_parameters: The parameters of
            the specified client method, for example,
            {'Bucket': 'your_bucket_name',
                'Key': 'folder_name/file_name.txt',}.
            ACL in this parameters will be ignored.
        :param expires_in: The number of seconds the
            presigned URL is valid for, for example, 3600.
        :param acl: S3ACL. For more info, pls check:
                https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
        :return: The presigned URL.
        """
        if acl:
            method_parameters["ACL"] = acl
        try:
            url = self.client.generate_presigned_url(
                ClientMethod=client_method,
                Params=method_parameters,
                ExpiresIn=expires_in,
            )
        except ClientError:
            print(
                "Couldn't get a presigned URL for client method '%s'.",
                client_method,
            )
            raise ClientError
        return url

    def check_url_exist(self, bucket_name: str, s3_key: str) -> bool:
        results = self.client.list_objects(Bucket=bucket_name, Prefix=s3_key)
        return "Contents" in results
