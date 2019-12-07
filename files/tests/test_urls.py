from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import assert_status_code


class StatusCodeTests(APITestCase):
  def test_user_files(self):
    url = reverse('user_files')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')


  def test_file_contents(self):
    url = reverse('file_contents', kwargs={'pk': 1})
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')


  def test_file_update_retrieve(self):
    url = reverse('file_update_retrieve', kwargs={'pk': 1})
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')


  def test_file_add(self):
    url = reverse('file_add')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'post')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'options')

    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'get')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'put')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'patch')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'delete')
    assert_status_code(self, url, s.HTTP_401_UNAUTHORIZED, 'head')

