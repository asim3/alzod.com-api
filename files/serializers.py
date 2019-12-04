from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import FileModel


class AddFileSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "fk_user", "fk_parent", "name", "photo", "is_public",)


class UpdateFileSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    depth = 1
    fields = ("fk_parent", "name", "photo", "is_public",)
    read_only_fields = (
      "pk",
      "fk_user",
      "children",
      "issue_date",
      "update_date",
      "delete_date",
    )

class UserFilesSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "name", "photo", "is_public",)


# ------------


class ParentSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "fk_parent", "name",)
    depth = 5


class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ("id", "username", "first_name", "last_name", "email",)
