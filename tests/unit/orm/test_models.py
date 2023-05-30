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
    async def get_user_by_id(self, id: int) -> User:
        sql = f"SELECT * FROM `user` WHERE `id` = {id}"
        users = await User.raw(sql)
        return users[0]

    async def test_tz_in_time_field(self, user_model):
        user = user_model(name="test1", email="test1@test.com")
        await user.save()
        assert user.created_at.tzinfo
        await user.delete()

        user2 = await self.get_user_by_id(user.id)
        assert user2

        print("user2.deleted_at.tzinfo", user2.deleted_at.tzinfo)
        assert user2.deleted_at.tzinfo

    @pytest.mark.anyio
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

    async def test_soft_delete(self, user_model):
        user = user_model(name="test4", email="test4@test.com")
        await user.save()
        assert user.id

        await user.delete()
        user2 = await self.get_user_by_id(user.id)
        assert user2

        assert user2.deleted_at

        assert abs(user2.deleted_at - user2.updated_at) < datetime.timedelta(
            seconds=1
        )

    async def test_soft_delete_with_filter(self, user_model):
        user = user_model(name="test5", email="test5@test.com")
        await user.save()
        assert user.id

        await user.delete()

        user2 = await user_model.filter(id=user.id).first()
        assert user2 is None

        users = await get_all_records_by_encrypted_field(
            user_model, "email", user.email
        )
        assert len(users) == 0

    async def test_soft_delete_with_encrypt_field(self, user_model):
        user = user_model(name="test6", email="test6@test.com")
        await user.save()
        assert user.id

        await user.delete()

        users = await get_all_records_by_encrypted_field(
            user_model, "email", user.email
        )
        assert len(users) == 0

    async def test_soft_delete_with_get(self, user_model):
        user = user_model(name="test6", email="test6@test.com")
        await user.save()
        assert user.id

        await user.delete()

        with pytest.raises(DoesNotExist):
            user2 = await user_model.get(id=user.id)
            assert not user2

    async def test_soft_delete_with_all(self, user_model):
        user = user_model(name="test1", email="test1@test.com")
        await user.save()
        assert user.id

        user1 = user_model(name="test2", email="test2@test.com")
        await user1.save()
        assert user1.id

        await user.delete()
        await user1.delete()

        users = await user_model.all()
        assert not users
