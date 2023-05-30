from apex_fastapi.aws.s3 import S3Client


class TestS3Client:
    async def test_get_presign_url(self, s3_client):
        client = S3Client()
        url = client.generate_presigned_url(
            "put_object",
            {"Bucket": "join-backend-test", "Key": "test"},
            3600,
        )
        assert url
