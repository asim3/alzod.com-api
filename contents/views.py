from rest_framework.generics import (
  ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView)
from .validators import is_fk_file_valid
from .serializers import ContentSerializer


class ListAddView(ListCreateAPIView):
  serializer_class = ContentSerializer

  def create(self, request, *args, **kwargs):
    is_fk_file_valid(request)
    return super().create(request, *args, **kwargs)


class UpdateView(RetrieveUpdateAPIView):
  serializer_class = ContentSerializer

  def update(self, request, *args, **kwargs):
    is_fk_file_valid(request, kwargs.get('pk'))
    return super().update(request, *args, **kwargs)

  def get_queryset(self):
    return self.request.user.files
