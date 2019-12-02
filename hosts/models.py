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


class HostModel(Model):
  name = CharField(max_length=300)
  issue_date = DateTimeField(auto_now_add=True)