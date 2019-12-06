from django.urls import path
from .views import (
  AddView,
  UpdateView,
  UserFilesView,
  FilesContentsView,
)


urlpatterns = [
  path('user/', UserFilesView.as_view(), name='user_files'),
  path('<int:pk>/contents/', FilesContentsView.as_view(), name='file_contents'),
  path('<int:pk>/', UpdateView.as_view(), name='file_update_retrieve'),
  path('', AddView.as_view(), name='file_add'),
]