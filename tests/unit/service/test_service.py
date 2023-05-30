from apex_fastapi.service import BaseService


def test_service():
    base_service = BaseService()
    assert base_service
