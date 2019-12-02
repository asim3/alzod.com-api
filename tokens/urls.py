from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TokenRenewView, register_view


urlpatterns = [
  path('refresh/', TokenRenewView.as_view(), name='token_refresh'),
  path('register/', register_view, name='register'),
  path('', TokenObtainPairView.as_view(), name='token_obtain'),
]