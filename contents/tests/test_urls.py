from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import assert_status_code


class StatusCodeTests(APITestCase):
  def test_content_update(self):
    url = reverse('content_update', kwargs={'pk': 1})
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')


  def test_content_add(self):
    url = reverse('content_add')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')

