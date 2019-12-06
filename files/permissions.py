from rest_framework.exceptions import ValidationError


def check_user_file_permissions(user, file_user):
  if not user or not file_user or user != file_user:
    err = "You do not have permissions on parent file."
    raise ValidationError({'fk_parent': [err]})
