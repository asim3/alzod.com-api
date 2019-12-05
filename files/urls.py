from django.urls import path
from .views import (
  AddView,
  UpdateView,
  UserFilesView,
)


urlpatterns = [
  path('user/', UserFilesView.as_view(), name='user_files'),
  path('add/', AddView.as_view(), name='file_add'),
  path('<int:pk>/', UpdateView.as_view(), name='file_update_retrieve'),
]