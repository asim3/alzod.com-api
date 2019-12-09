from rest_framework.exceptions import ValidationError


def check_user_file_permissions(request_user, file_user):
  if not request_user or not file_user or request_user != file_user:
    err = "You do not have permissions on parent file."
    raise ValidationError({'fk_parent': [err]})
