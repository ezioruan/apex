from tortoise import fields

from .models import BaseModel, EncryptedField

# # The following code is just an example to show how to operate the model
#
# # Create a new user
# user = User(name='user1', email='user1@gmail.com')
# await User.save()
#
# # Get the user by id
# user2 = await User.filter(id=user.id).first()
#
# # Get the user by an encrypted field
# users = await get_all_records_by_encrypted_field(
#     User, 'email', 'client2@gmail.com')


class User(BaseModel):
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)

    class Meta:
        table = "user"
        ordering = ["id"]
