from django.urls import path
from .views import AddView, UpdateView, DeleteView


urlpatterns = [
  # path('<int:fk_file>/add/', AddView.as_view(), name='contributor_add'),
  # path('<int:fk_file>/update/', UpdateView.as_view(), name='contributor_update'),
  # path('<int:fk_file>/delete/', DeleteView.as_view(), name='contributor_delete'),
]