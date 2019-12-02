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


class FileModel(Model):
  fk_host = ForeignKey("hosts.HostModel", on_delete=CASCADE)
  fk_parent = ForeignKey("self", on_delete=CASCADE, null=True)
  
  name = CharField(max_length=300)
  photo = ImageField(upload_to="files/", blank=True, null=True)
  is_public = BooleanField(default=False)
  issue_date = DateTimeField(auto_now_add=True)
  update_date = DateTimeField(auto_now=True)