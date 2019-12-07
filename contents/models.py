from django.db import models
from django.db.models import (
  Model,
  BigAutoField,
  ForeignKey,
  CharField,
  BooleanField,
  DateTimeField,
  DateField,
  TextField,
  CASCADE,
)


class ContentModel(Model):
  id = BigAutoField(primary_key=True)
  fk_file = ForeignKey("files.FileModel", on_delete=CASCADE, related_name="contents")
  
  content_type = CharField(max_length=1)
  text = TextField()

  class Meta:
    ordering = ["id"]
  
  # content_type = CharField(max_length=2)
  # text = CharField(max_length=1000)