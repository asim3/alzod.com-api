from django.urls import path
from .views import (
  AddView,
  UpdateView,
  DeleteView,
  DisplayView,
)


urlpatterns = [
  path('add/', AddView.as_view(), name='file_add'),
  path('<int:pk>/update/', UpdateView.as_view(), name='file_update'),
  path('<int:pk>/delete/', DeleteView.as_view(), name='file_delete'),
  path('<int:pk>/', DisplayView.as_view(), name='file_display'),
]