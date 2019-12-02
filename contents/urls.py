from django.urls import path
from .views import (
  AddView,
  UpdateView,
  DeleteView,
)


urlpatterns = [
  # path('<int:pk>/add/', AddView.as_view(), name='content_add'),
  # path('<int:pk>/update/', UpdateView.as_view(), name='content_update'),
  # path('<int:pk>/delete/', DeleteView.as_view(), name='content_delete'),
]