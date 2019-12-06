from django.urls import path
from .views import (
  ListAddView,
  UpdateView,
)


urlpatterns = [
  path('<int:file_pk>/', ListAddView.as_view(), name='content_list_add'),
  path('<int:file_pk>/<int:content_pk>/', UpdateView.as_view(), name='content_update'),
]