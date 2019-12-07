from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import StatusCodeTest


# class CheckStatusCode(APITestCase):
#   def test_token_refresh(self):
#     url = reverse('token_refresh')
#     asert = StatusCodeTest(self, url)
#     asert.status_code('post', s.HTTP_400_BAD_REQUEST)
#     asert.status_code('options', s.HTTP_200_OK)

#     asert.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
#     asert.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
#     asert.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
#     asert.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
#     asert.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)

