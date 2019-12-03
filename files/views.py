from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from .serializers import FileSerializer
from .models import FileModel


class AddView(CreateAPIView):
  serializer_class = FileSerializer

  def create(self, request, *args, **kwargs):
    request.data['fk_user'] = request.user.id
    return super().create(request, *args, **kwargs)


class UpdateView(UpdateAPIView):
  serializer_class = FileSerializer

  def get_queryset(self):
    return FileModel.objects.filter(fk_user=self.request.user)