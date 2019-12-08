from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import (
  Model, CASCADE, BigAutoField, ForeignKey, BooleanField, CharField,
  ImageField, DateTimeField, DateField,
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

  class Meta:
    ordering = ["id"]

  def __str__(self):
    if self.fk_parent:
      return f"{self.fk_parent.id} / {self.id} - {self.name}"
    return f"/ {self.id} - {self.name}"

  def parents_ids(self):
    """
      For Validation Checks
    """
    if self.fk_parent:
      all_parents_ids = self.fk_parent.parents_ids()
      if all_parents_ids:
        return [*all_parents_ids, self.fk_parent.id]
      return [self.fk_parent.id]

  def clean(self):
    if self.fk_parent:
      err = "File cannot be parent of himself."
      if self.pk == self.fk_parent.pk:
        raise ValidationError({'fk_parent': err})
    
      if 9 < self.fk_parent.children.count():
        raise ValidationError({
          'fk_parent': "Parent file reached maximum allowed files."})

      parents_ids = self.parents_ids()
      if parents_ids:
        if self.pk in parents_ids:
          raise ValidationError({'fk_parent': err})

  def parents_as_list(self, i=1):
    if self.fk_parent and i < 5:
      all_parents = self.fk_parent.parents_as_list(i + 1)
      parent = {"order": i, "id":self.fk_parent.id,"name":self.fk_parent.name}
      if all_parents:
        return [*all_parents, parent]
      return [parent]

  def user_as_dict(self):
    full_name = self.fk_user.first_name + " " + self.fk_user.last_name
    return {
      "id": self.fk_user.pk,
      "username": self.fk_user.username,
      "name": full_name.strip(),
      "email": self.fk_user.email
    }

  def children_as_list(self):
    data = []
    for child in self.children.all():
      child_photo = child.photo or {"url": "http://localhost:8000/"}
      data.append({
        "id": child.pk,
        "name": child.name,
        "photo": child_photo.get("url"),
        "is_public": child.is_public
      })
    return data