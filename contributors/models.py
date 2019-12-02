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


class ContributorModel(Model):
  fk_file = ForeignKey("files.FileModel", on_delete=CASCADE)
  fk_user = ForeignKey(User, on_delete=CASCADE)

  active = BooleanField(default=False)
  can_read_private = BooleanField(default=False)

  can_update = BooleanField(default=False)
  can_remove = BooleanField(default=False)
  can_update_contributors = BooleanField(default=False)
  can_remove_contributors = BooleanField(default=False)
