from rest_framework.exceptions import ValidationError
from .models import FileModel
from .permissions import check_user_file_permissions


def check_maximum_allowed_files(total):
  max_length = 9
  if total:
    if max_length <= total:
      err = "Parent file reached maximum allowed files."
      raise ValidationError({'fk_parent': [err]})


def check_duplicate_parent_id(pk, parent_pk, parents_ids):
  err = "File cannot be parent of himself."
  if pk == parent_pk:
    raise ValidationError({'fk_parent': [err]})

  if parents_ids:
    if pk in parents_ids:
      raise ValidationError({'fk_parent': [err]})


def is_fk_parent_valid(request, kwargs_pk=None):
  fk_parent = request.data.get('fk_parent')
  if fk_parent:
    if not isinstance(fk_parent, int):
      raise ValidationError({'fk_parent': ["Invalid file id."]})
    try:
      parent = FileModel.objects.get(pk=fk_parent)
    except FileModel.DoesNotExist:
      err = "Parent file does not exist."
      raise ValidationError({'fk_parent': [err]})
    
    check_maximum_allowed_files(parent.children.count())
    check_duplicate_parent_id(kwargs_pk, parent.pk, parent.parents_ids())
    check_user_file_permissions(parent.fk_user, request.user)
  return True
