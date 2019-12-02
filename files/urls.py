from django.urls import path
from .views import (
  AddFileView,
  AddBranchFileView,
  DeleteFileView,
  FileContentsView,
)


urlpatterns = [
  # path('add/', AddFileView.as_view(), name='file_add'),
  # path('<int:pk>/add/', AddBranchFileView.as_view(), name='file_add_branch'),
  # path('<int:pk>/delete/', DeleteFileView.as_view(), name='file_delete'),
  # path('<int:pk>/', FileContentsView.as_view(), name='file_contents'),
]