from rest_framework.serializers import ModelSerializer
from .models import FileModel
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = (
      "id",
      "username",
      "first_name",
      "last_name",
      "email",
    )
    # read_only_fields = ['account_name']
    depth = 3


class FileSerializer(ModelSerializer):
  fk_user = UserSerializer()

  class Meta:
    model = FileModel
    fields = (
      "pk",
      "fk_user",
      "fk_parent",
      "name",
      "photo",
      "is_public",
    )
    # read_only_fields = ['account_name']
    depth = 1