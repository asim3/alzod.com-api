from django.urls import path
from .views import (
  AddView,
  UpdateView,
  ListUserFilesView,
)


urlpatterns = [
  path('user/', ListUserFilesView.as_view(), name='list_user_files'),
  path('add/', AddView.as_view(), name='file_add'),
  path('<int:pk>/', UpdateView.as_view(), name='file_update_retrieve'),
]