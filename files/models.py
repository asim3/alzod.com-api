from django.db import models


class FilesModel(models.Model):
  parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=300)
  photo = models.ImageField(upload_to="/files/", blank=True, null=True)
  owner = models.ForeignKey("User", on_delete=models.CASCADE)
  public = models.DateField()
  issue_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)