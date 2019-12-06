from django.contrib.auth.models import User
from rest_framework.serializers import ( 
  Serializer, ModelSerializer, ValidationError, BooleanField, IntegerField,
  DecimalField, CharField, EmailField, ChoiceField, MultipleChoiceField,
  DateTimeField, DateField, FileField, ImageField, SerializerMethodField,
  ListField, DictField, HiddenField, CreateOnlyDefault,
)
from .models import ContentModel


class ContentSerializer(ModelSerializer):
  # A `HiddenField` does not take input from the user, or present any output
  fk_file = HiddenField(default=CreateOnlyDefault())

  class Meta:
    model = ContentModel
    fields = ("content_type", "text",)