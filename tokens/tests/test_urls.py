from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase


class StatusCodeTest:
  def __init__(self, cls, url):
    self.test_class = cls
    self.client = cls.client
    self.url = url

  def get_response(self, request_type):
    return getattr(self.client, request_type)

  def status_code(self, request_type, status_code, data={}):
    _response = self.get_response(request_type)
    response = _response(self.url, data, format='json')
    self.test_class.assertEqual(response.status_code, status_code)


class UserStatusCodeTest(StatusCodeTest):
  def __init__(self, cls, url):
    self.test_class = cls
    self.client = cls.client
    self.user = User.objects.create_user("test1", password="1234sdfsdkfsfA")
    self.client.force_authenticate(user=self.user)
    self.url = url


class CheckStatusCode(APITestCase):
  def test_register(self):
    register = StatusCodeTest(self, reverse('register'))
    register.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)
    register.status_code('options', s.HTTP_405_METHOD_NOT_ALLOWED)
    
    register.status_code('post', s.HTTP_400_BAD_REQUEST)


  def test_token_obtain(self):
    url = reverse('token_obtain')
    token_obtain = StatusCodeTest(self, url)
    token_obtain.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_obtain.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_obtain.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_obtain.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_obtain.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)

    token_obtain.status_code('post', s.HTTP_400_BAD_REQUEST)
    token_obtain.status_code('options', s.HTTP_200_OK)



  def test_token_refresh(self):
    token_refresh = StatusCodeTest(self, reverse('token_refresh'))
    token_refresh.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_refresh.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_refresh.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_refresh.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
    token_refresh.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)

    token_refresh.status_code('post', s.HTTP_400_BAD_REQUEST)
    token_refresh.status_code('options', s.HTTP_200_OK)