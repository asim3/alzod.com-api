from rest_framework.serializers import ( 
  Serializer, ModelSerializer, ValidationError, BooleanField, IntegerField,
  DecimalField, CharField, EmailField, ChoiceField, MultipleChoiceField,
  DateTimeField, DateField, FileField, ImageField, SerializerMethodField,
  ListField, DictField, HiddenField, CreateOnlyDefault,
)
from .models import ContentModel


class ContentSerializer(ModelSerializer):
  class Meta:
    model = ContentModel
    fields = ("pk", "fk_file", "content_type", "text",)