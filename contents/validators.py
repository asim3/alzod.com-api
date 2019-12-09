from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from files.models import FileModel
from files.permissions import check_user_file_permissions
from .models import ContentModel


def is_fk_file_valid(request, kwargs_pk=None):
  if kwargs_pk:
    try:
      content = ContentModel.objects.get(pk=kwargs_pk)
    except ContentModel.DoesNotExist:
      raise NotFound()

    content_user = content.fk_file.fk_user
    check_user_file_permissions(request.user, content_user)
  
  data_file = request.data.get('fk_file')
  if data_file:
    if not isinstance(data_file, int):
      raise ValidationError({'fk_file': ["File id invalid."]})
    try:
      parent = FileModel.objects.get(pk=data_file)
    except FileModel.DoesNotExist:
      err = "Parent file does not exist."
      raise ValidationError({'fk_file': [err]})

    parent_user = parent.fk_user
    check_user_file_permissions(request.user, parent_user)
  return True