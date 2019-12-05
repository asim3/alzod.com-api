from django.contrib.auth.models import User
from rest_framework.serializers import ( 
  Serializer, ModelSerializer, ValidationError, BooleanField, IntegerField,
  DecimalField, CharField, EmailField, ChoiceField, MultipleChoiceField,
  DateTimeField, DateField, FileField, ImageField, SerializerMethodField,
  ListField, DictField,CurrentUserDefault,HiddenField
)
from .models import ContentModel


class ContentSerializer(ModelSerializer):
  class Meta:
    model = ContentModel
    fields = ("content_type", "text",)