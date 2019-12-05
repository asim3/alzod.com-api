from rest_framework.exceptions import ValidationError
from .models import ContentModel


def is_fk_file_valid(request, kwargs_pk=None):
  fk_file = request.data.get('fk_file')
  if fk_file:
    if not isinstance(fk_file, int):
      raise ValidationError({'fk_file': ["Invalid file id."]})
    try:
      parent = ContentModel.objects.get(pk=fk_file)
    except ContentModel.DoesNotExist:
      err = "Parent file does not exist."
      raise ValidationError({'fk_file': [err]})
    
  return True