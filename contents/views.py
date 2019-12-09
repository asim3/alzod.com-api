from rest_framework.exceptions import ValidationError, NotFound, NotAuthenticated, AuthenticationFailed
from rest_framework.generics import (
  CreateAPIView, RetrieveUpdateAPIView, ListAPIView)
from .validators import is_fk_file_valid
from .serializers import ContentSerializer
from .models import ContentModel

class AddView(CreateAPIView):
  serializer_class = ContentSerializer

  def create(self, request, *args, **kwargs):
    is_fk_file_valid(request)
    return super().create(request, *args, **kwargs)

  def get_queryset(self):
    file_pk = self.kwargs.get("pk")
    return self.request.user.files.filter(pk=file_pk)

class UpdateView(RetrieveUpdateAPIView):
  serializer_class = ContentSerializer
  queryset = ContentModel

  def update(self, request, *args, **kwargs):
    is_fk_file_valid(request, self.kwargs.get('pk'))
    return super().update(request, *args, **kwargs)

  def retrieve(self, request, *args, **kwargs):
    is_fk_file_valid(request, self.kwargs.get('pk'))
    return super().retrieve(request, *args, **kwargs)