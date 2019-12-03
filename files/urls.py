from django.urls import path
from .views import (
  AddView,
  UpdateView,
  ListFileContentsView,
  ListUserFilesView,
)


urlpatterns = [
  path('add/', AddView.as_view(), name='file_add'),
  path('<int:pk>/update/', UpdateView.as_view(), name='file_update'),
  path('<int:pk>/', ListFileContentsView.as_view(), name='list_file_contents'),
  path('', ListUserFilesView.as_view(), name='list_user_files'),
]