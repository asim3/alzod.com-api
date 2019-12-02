from django.contrib.auth.models import User
from django.db.models import (
  Model,
  ForeignKey,
  CharField,
  ImageField,
  BooleanField,
  DateTimeField,
  CASCADE,
)


class GuestModel(Model):
  fk_host = ForeignKey("files.HostModel", on_delete=CASCADE)
  fk_user = ForeignKey(User, on_delete=CASCADE)

  active = BooleanField()
  can_read = BooleanField()
  can_write = BooleanField()
  can_remove = BooleanField()
