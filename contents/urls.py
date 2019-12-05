from django.urls import path
from .views import (
  AddView,
  UpdateView,
)


urlpatterns = [
  path('<int:file_pk>/', AddView.as_view(), name='content_add'),
  path('<int:file_pk>/<int:content_pk>/', UpdateView.as_view(), name='content_update'),
]