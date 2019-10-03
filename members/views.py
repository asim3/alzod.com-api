from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from alzod.permissions import ReadOnly
from .serializers import AuthSerializer, UserSerializer


class AuthUserView(ListModelMixin, GenericViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = AuthSerializer
    queryset = User.objects.all()

    @method_decorator(ensure_csrf_cookie)
    def list(self, request, *args, **kwargs):
        queryset = User.objects.first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(LoginView):
    template_name="index.html"
