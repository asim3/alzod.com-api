from django.http import Http404
from rest_framework.generics import (
  CreateAPIView, RetrieveUpdateAPIView, ListAPIView)
from .validators import is_fk_parent_valid
from .serializers import FileSerializer
from contents.serializers import ContentSerializer

class AddView(CreateAPIView):
  serializer_class = FileSerializer

  def create(self, request, *args, **kwargs):
    is_fk_parent_valid(request)
    return super().create(request, *args, **kwargs)


class UpdateView(RetrieveUpdateAPIView):
  serializer_class = FileSerializer

  def update(self, request, *args, **kwargs):
    is_fk_parent_valid(request, kwargs.get('pk'))
    return super().update(request, *args, **kwargs)

  def get_queryset(self):
    return self.request.user.files.all()


class UserFilesView(ListAPIView):
  serializer_class = FileSerializer

  def get_queryset(self):
    return self.request.user.files.filter(fk_parent__isnull=True)


class FilesContentsView(ListAPIView):
  serializer_class = ContentSerializer

  def get_queryset(self):
    pk = self.kwargs.get("pk")
    try:
      data = self.request.user.files.get(pk=pk)
    except:
      raise Http404()
    return data.contents.all()