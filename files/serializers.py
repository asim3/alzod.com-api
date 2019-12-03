from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import FileModel


class ParentSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "fk_parent", "name",)
    depth = 5


class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ("id", "username", "first_name", "last_name", "email",)


class AddFileSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "fk_user", "fk_parent", "name", "photo", "is_public",)


class UpdateFileSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "fk_parent", "name", "photo", "is_public",)
    read_only_fields = ['fk_user']


class ListUserFilesSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ("pk", "name", "photo", "is_public", "issue_date")
    depth = 5


class ListFileContentsSerializer(ModelSerializer):
  class Meta:
    model = FileModel
    fields = ()
    read_only_fields = ("pk", "fk_user", "fk_parent", "name", "photo", "is_public",)
