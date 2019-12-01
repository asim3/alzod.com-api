from django.db import models
from django.contrib.auth.models import User


class FilesModel(models.Model):
  parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=300)
  photo = models.ImageField(upload_to="files/", blank=True, null=True)
  public = models.models.BooleanField(default=False)
  issue_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)