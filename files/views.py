from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from .validators import is_fk_parent_valid
from .serializers import (
  AddFileSerializer,
  UpdateFileSerializer,
  UserFilesSerializer,
)


class AddView(CreateAPIView):
  serializer_class = AddFileSerializer

  def create(self, request, *args, **kwargs):
    request.data['fk_user'] = request.user.id
    is_fk_parent_valid(request)
    return super().create(request, *args, **kwargs)


class UpdateView(RetrieveUpdateAPIView):
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