from rest_framework.generics import (
  CreateAPIView, RetrieveUpdateAPIView, ListAPIView)
from .validators import is_fk_parent_valid
from .serializers import FileSerializer


class AddView(CreateAPIView):
  serializer_class = FileSerializer

  def create(self, request, *args, **kwargs):
    is_fk_parent_valid(request)
    return super().create(request, *args, **kwargs)


class UpdateView(RetrieveUpdateAPIView):
  serializer_class = FileSerializer

  def get_queryset(self):
    return self.request.user.files

  def update(self, request, *args, **kwargs):
    is_fk_parent_valid(request, kwargs.get('pk'))
    return super().update(request, *args, **kwargs)


class UserFilesView(ListAPIView):
  serializer_class = FileSerializer

  def get_queryset(self):
    return self.request.user.files.all()