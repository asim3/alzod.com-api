from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from .models import FileModel
from .validators import is_fk_parent_valid
from .serializers import (
  AddFileSerializer,
  UpdateFileSerializer,
  UserFilesSerializer,
  FileContentsSerializer,
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


class ListUserFilesView(ListAPIView):
  serializer_class = UserFilesSerializer

  def get_queryset(self):
    return self.request.user.files.all()


# ------------


class ListFileContentsView(ListAPIView):
  serializer_class = FileContentsSerializer

  def get_queryset(self):
    # get cheldern 
    # get all content
    # get parent list
    return self.request.user.files.all()