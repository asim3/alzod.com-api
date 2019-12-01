from django.db import models


class ContentsModel(models.Model):
  fk_file = models.ForeignKey("files.FilesModel", on_delete=models.CASCADE)
  content_type = models.CharField(max_length=1)
  text = models.TextField(blank=True, null=True)