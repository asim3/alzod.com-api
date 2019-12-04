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
    fields = ("pk", "fk_parent", "name", "photo", "is_public",)
    read_only_fields = ['fk_user']


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


class FileContentsSerializer(ModelSerializer):
  # import from content.serializer
  
  class Meta:
    model = FileModel
    fields = ("contents", "children", "parents", "name", "photo", "is_public",)
    depth = 0
