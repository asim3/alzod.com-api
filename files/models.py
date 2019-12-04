from django.core.exceptions import ValidationError
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
  fk_parent = ForeignKey("self", on_delete=CASCADE, related_name="children", blank=True, null=True,)
  fk_user = ForeignKey(User, on_delete=CASCADE, related_name="files")
  
  name = CharField(max_length=300)
  photo = ImageField(upload_to="files/", blank=True, null=True)
  is_public = BooleanField(default=False)
  issue_date = DateTimeField(auto_now_add=True)
  update_date = DateTimeField(auto_now=True)
  delete_date = DateField(blank=True, null=True)

  def __str__(self):
    parent = self.fk_parent or ""
    name = self.name
    if len(name) > 11:
      name = self.name[:11].strip() + "..."
    return f"{parent}/{name}"


  def parents(self):
    if self.fk_parent:
      _parents = self.fk_parent.parents()
      if _parents:
        return [*_parents, self.fk_parent.name]
      return [self.fk_parent.name]


  def parents_ids(self):
    if self.fk_parent:
      _parents_ids = self.fk_parent.parents_ids()
      if _parents_ids:
        return [*_parents_ids, self.fk_parent.id]
      return [self.fk_parent.id]


  def clean(self):
    err = "File cannot be parent of himself."
    if self.pk == self.fk_parent.pk:
      raise ValidationError({'fk_parent': err})
    
    parents_ids = self.parents_ids()
    if parents_ids:
      if self.pk in parents_ids:
        raise ValidationError({'fk_parent': err})