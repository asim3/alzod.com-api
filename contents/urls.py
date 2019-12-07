from django.urls import path
from .views import AddView, UpdateView


urlpatterns = [
  path('<int:pk>/', UpdateView.as_view(), name='content_update'),
  path('', AddView.as_view(), name='content_add'),
]