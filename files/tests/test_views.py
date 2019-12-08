from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import StatusCodeTest, UserStatusCodeTest
from files.models import FileModel
from tokens.tests.test_token_obtain import get_new_registered_user_tokens



data = get_new_registered_user_tokens()
refresh = data.get('refresh')
access = data.get('access')