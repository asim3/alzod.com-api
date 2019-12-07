from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import assert_status_code


# class StatusCodeTests(APITestCase):
#   def test_token_refresh(self):
#     url = reverse('token_refresh')
#     assert_status_code(self, url, s.HTTP_400_BAD_REQUEST, 'post')
#     assert_status_code(self, url, s.HTTP_200_OK, 'options')

#     assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'get')
#     assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'put')
#     assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'patch')
#     assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'delete')
#     assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'head')

