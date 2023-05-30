import datetime

import pytest
from tortoise.exceptions import DoesNotExist

from apex_fastapi.orm.helper import get_all_records_by_encrypted_field
from apex_fastapi.orm.test_models import User


@pytest.fixture(scope="session")
async def user_model(db):
    yield User
    await User.raw("delete from `user`")


@pytest.mark.asyncio
class TestORM:
    async def test_tz_in_time_field(self, user_model):
        user = user_model(name="test1", email="test1@test.com")
        await user.save()
        assert user.created_at.tzinfo

    async def test_create_and_find_by_id(self, user_model):
        user = user_model(name="test2", email="test2@test.com")
        await user.save()
        assert user.id
        user2 = await user_model.filter(id=user.id).first()
        assert user.name == user2.name
        assert user.email == user2.email
        assert user.created_at
        assert user.updated_at
        await user.delete()

    async def test_create_and_find_by_email(self, user_model):
        user = user_model(name="test3", email="test3@test.com")
        await user.save()
        assert user.id
        users = await get_all_records_by_encrypted_field(
            user_model, "email", user.email
        )
        assert len(users) == 1
        user2 = users[0]
        assert user.name == user2.name
        assert user.email == user2.email
        assert user.created_at
        assert user.updated_at
        await user.delete()
