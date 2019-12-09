from rest_framework.exceptions import ValidationError, NotFound, NotAuthenticated, AuthenticationFailed
from files.models import FileModel
from files.permissions import check_user_file_permissions
from .models import ContentModel


def is_fk_file_valid(request, kwargs_pk=None):
  if kwargs_pk:
    try:
      content = ContentModel.objects.get(pk=kwargs_pk)
    except ContentModel.DoesNotExist:
      raise NotFound(detail="kwargs_pk")

    content_user = content.fk_file.fk_user
    check_user_file_permissions(request.user, content_user)
  
  print(request.data)
  return True