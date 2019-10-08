from rest_framework.serializers import Serializer, ModelSerializer, ReadOnlyField
from django.contrib.auth.models import User


class AuthSerializer(Serializer):
    id = ReadOnlyField(default="no")
    type = ReadOnlyField(default="user")
    auth = ReadOnlyField(source="is_authenticated", default="no")
    username = ReadOnlyField(default="gest")
    img = ReadOnlyField(default="img/img.img")
    


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
