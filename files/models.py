from django.contrib.auth.models import User
from django.db.models import (
  Model,
  BigAutoField,
  ForeignKey,
  CharField,
  ImageField,
  BooleanField,
  DateTimeField,
  DateField,
  CASCADE,
)


class FileModel(Model):
  id = BigAutoField(primary_key=True)
  fk_parent = ForeignKey("self", on_delete=CASCADE, blank=True, null=True)
  fk_user = ForeignKey(User, on_delete=CASCADE, related_name="files")
  
  name = CharField(max_length=300)
  photo = ImageField(upload_to="files/", blank=True, null=True)
  is_public = BooleanField(default=False)
  issue_date = DateTimeField(auto_now_add=True)
  update_date = DateTimeField(auto_now=True)
  delete_date = DateField(blank=True, null=True)