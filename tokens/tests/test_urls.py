from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase


def assert_status_code(self, url, status_code, request_type, data={}):
  response = getattr(self.client, request_type)(url, data, format='json')
  self.assertEqual(response.status_code, status_code)


class StatusCodeTests(APITestCase):
  def test_register(self):
    url = reverse('register')
    assert_status_code(self, url, s.HTTP_400_BAD_REQUEST, 'post')

    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'get')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'put')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'patch')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'delete')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'head')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'options')


  def test_token_obtain(self):
    url = reverse('token_obtain')
    assert_status_code(self, url, s.HTTP_400_BAD_REQUEST, 'post')
    assert_status_code(self, url, s.HTTP_200_OK, 'options')

    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'get')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'put')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'patch')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'delete')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'head')


  def test_token_refresh(self):
    url = reverse('token_refresh')
    assert_status_code(self, url, s.HTTP_400_BAD_REQUEST, 'post')
    assert_status_code(self, url, s.HTTP_200_OK, 'options')

    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'get')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'put')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'patch')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'delete')
    assert_status_code(self, url, s.HTTP_405_METHOD_NOT_ALLOWED, 'head')

