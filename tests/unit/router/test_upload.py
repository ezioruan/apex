import os

import pytest

from apex_fastapi.router.upload import PreSignUrlRequest, S3PreSignedUrl


@pytest.mark.asyncio
class TestUpload:
    def setup(self):
        self.file_name = "demo.pdf"
        self.dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.file_path = os.path.join(self.dir, "data", self.file_name)
        self.inVo = PreSignUrlRequest(file_name=self.file_name)
        self.client = S3PreSignedUrl()
        self.bucket_name = "join-backend-test"

    async def test_generate_presigned_url(self, s3_client):
        presigned_url = await self.client.generate_presigned_url(
            self.inVo, self.bucket_name
        )
        assert presigned_url.url
        assert presigned_url.fields
        assert presigned_url.s3_key
