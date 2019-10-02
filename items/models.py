from django.db import models

class Item(models.Model):
  type = models.CharField(max_length=10)
  title = models.CharField(max_length=100)
  img = models.ImageField(upload_to="image_path/", blank=True, null=True)
  add_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  price = models.IntegerField(blank=True,null=True)
  country = models.CharField(max_length=3, blank=True, null=True)
  currency = models.CharField(max_length=3, blank=True, null=True)
  description = models.TextField(blank=True, null=True)