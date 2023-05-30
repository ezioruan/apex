from tortoise.manager import Manager


class EnabledObjectManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)
