from django.db import models
from django.db.models import (
  Model,
  ForeignKey,
  CharField,
  BooleanField,
  DateTimeField,
  TextField,
  CASCADE,
)


class ContentModel(Model):
  fk_file = ForeignKey("files.FileModel", on_delete=CASCADE)
  
  content_type = CharField(max_length=1)
  text = TextField(blank=True, null=True)