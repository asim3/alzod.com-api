from rest_framework.serializers import ( 
  Serializer, ModelSerializer, ValidationError, BooleanField, IntegerField,
  DecimalField, CharField, EmailField, ChoiceField, MultipleChoiceField,
  DateTimeField, DateField, FileField, ImageField, SerializerMethodField,
  ListField, DictField, HiddenField, CurrentUserDefault,
)
from .models import FileModel


class FileSerializer(ModelSerializer):
  name = CharField(max_length=300)
  photo = ImageField(required=False)
  is_public = BooleanField(required=False)
  delete_date = DateField(required=False)
  # read_only
  pk = IntegerField(read_only=True)
  issue_date = DateTimeField(read_only=True)
  update_date = DateTimeField(read_only=True)
  user_as_dict = DictField(read_only=True)
  parents_as_list = ListField(read_only=True)
  children_as_list = ListField(read_only=True)
  # A `HiddenField` does not take input from the user, or present any output
  fk_user = HiddenField(default=CurrentUserDefault())

  class Meta:
    model = FileModel
    fields = (
      "pk",
      "fk_parent",
      "name",
      "photo",
      "is_public",
      "issue_date",
      "update_date",
      "delete_date",
      "user_as_dict",
      "parents_as_list",
      "children_as_list",
      "fk_user",
    )