from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.exceptions import ValidationError
from .models import FileModel
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
    return super().create(request, *args, **kwargs)

  def perform_create(self, serializer):
    fk_parent = serializer.data.get('fk_parent')
    if fk_parent:
      parent_user = FileModel.objects.get(pk=fk_parent).fk_user.pk
      
      request_user = self.request.user.id
      fk_user = serializer.data.get('fk_user')
      
      raise ValidationError(f"aaaa {parent_user} {request_user}")
    serializer.save()


class UpdateView(UpdateAPIView):
  serializer_class = UpdateFileSerializer

  def get_queryset(self):
    return self.request.user.files

  def perform_update(self, serializer):
    fk_parent = serializer.data.get('fk_parent')
    if fk_parent:
      request_user = self.request.user.id
      raise ValidationError(f"aaaa {fk_parent} {request_user}")
    serializer.save()
    

class ListFileContentsView(ListAPIView):
  serializer_class = ListFileContentsSerializer

  def get_queryset(self):
    return self.request.user.files.all()


class ListUserFilesView(ListAPIView):
  serializer_class = ListUserFilesSerializer

  def get_queryset(self):
    return self.request.user.files.all()