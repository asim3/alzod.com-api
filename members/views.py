from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from alzod.permissions import ReadOnly
from .serializers import AuthSerializer, UserSerializer


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_redirect_url())

    def form_invalid(self, form):
        return HttpResponseBadRequest(
            '{"username": "cc"}',
            content_type="application/json"
        )

    def get_redirect_url(self):
        return "/api/auth/"


class UserLogoutView(LogoutView):
    next_page = "/api/auth/"