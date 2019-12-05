from django.contrib.auth.models import User
from rest_framework.serializers import ( 
  Serializer, ModelSerializer, ValidationError, BooleanField, IntegerField,
  DecimalField, CharField, EmailField, ChoiceField, MultipleChoiceField,
  DateTimeField, DateField, FileField, ImageField, SerializerMethodField,
  ListField, DictField,CurrentUserDefault,HiddenField
)
from .models import FileModel


class FileSerializer(ModelSerializer):
  name = CharField(max_length=300)
  photo = ImageField(required=False)
  is_public = BooleanField(required=False)
  delete_date = DateField(required=False)
  fk_user = HiddenField(default=CurrentUserDefault())
  # read_only
  pk = IntegerField(read_only=True)
  issue_date = DateTimeField(read_only=True)
  update_date = DateTimeField(read_only=True)
  user_as_dict = DictField(read_only=True)
  parents_as_list = ListField(read_only=True)
  children_as_list = ListField(read_only=True)

  class Meta:
    model = FileModel
    fields = (
      "pk",
      "fk_parent",
      "fk_user",
      "name",
      "photo",
      "is_public",
      "issue_date",
      "update_date",
      "delete_date",
      "user_as_dict",
      "parents_as_list",
      "children_as_list",
    )