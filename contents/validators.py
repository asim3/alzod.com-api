from rest_framework.exceptions import ValidationError
from .models import ContentModel
from files.models import FileModel
from files.permissions import check_user_file_permissions


def is_fk_file_valid(request, kwargs_pk=None):
  if kwargs_pk:
    current_file_model = ContentModel.objects.get(pk=kwargs_pk).fk_file
    check_user_file_permissions(request.user, current_file_model.fk_user)

  file_pk = request.data.get('fk_file')
  if file_pk:
    if not isinstance(file_pk, int):
      raise ValidationError({'fk_file': ["Invalid file id.."]})
    try:
      file_model = FileModel.objects.get(pk=file_pk)
    except FileModel.DoesNotExist:
      err = "File file does not exist."
      raise ValidationError({'fk_file': [err]})
    check_user_file_permissions(request.user, file_model.fk_user)
  return True