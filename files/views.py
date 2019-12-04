from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from .models import FileModel
from .validators import is_fk_parent_valid
from .serializers import (
  AddFileSerializer,
  UpdateFileSerializer,
  ListFileContentsSerializer,
  ListUserFilesSerializer,
)


class AddView(CreateAPIView):
  serializer_class = AddFileSerializer

  def create(self, request, *args, **kwargs):
    request.data['fk_user'] = request.user.id
    is_fk_parent_valid(request)
    return super().create(request, *args, **kwargs)


class UpdateView(UpdateAPIView):
  serializer_class = UpdateFileSerializer

  def get_queryset(self):
    return self.request.user.files

  def update(self, request, *args, **kwargs):
    is_fk_parent_valid(request, kwargs.get('pk'))
    return super().update(request, *args, **kwargs)
    

class ListFileContentsView(ListAPIView):
  serializer_class = ListFileContentsSerializer

  def get_queryset(self):
    return self.request.user.files.all()


class ListUserFilesView(ListAPIView):
  serializer_class = ListUserFilesSerializer

  def get_queryset(self):
    return self.request.user.files.all()