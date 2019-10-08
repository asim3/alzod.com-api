from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from alzod.permissions import ReadOnly
from .serializers import AuthSerializer, UserSerializer

class AuthUserView(ListModelMixin, GenericViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = AuthSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = request.user
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_redirect_url())

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_redirect_url())

    def get_redirect_url(self):
        return "/api/auth/"


class UserLogoutView(LogoutView):
    next_page = "/api/auth/"