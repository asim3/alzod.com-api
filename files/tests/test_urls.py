from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import StatusCodeTest, UserStatusCodeTest
from files.models import FileModel

class CheckStatusCode(APITestCase):
  def test_user_files(self):
    url = reverse('user_files')
    user_files = StatusCodeTest(self, url)
    user_files.status_code('options', s.HTTP_401_UNAUTHORIZED)
    user_files.status_code('get', s.HTTP_401_UNAUTHORIZED)

    user_files.status_code('post', s.HTTP_401_UNAUTHORIZED)
    user_files.status_code('put', s.HTTP_401_UNAUTHORIZED)
    user_files.status_code('patch', s.HTTP_401_UNAUTHORIZED)
    user_files.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    user_files.status_code('head', s.HTTP_401_UNAUTHORIZED)

    user_user_files = UserStatusCodeTest(self, url)
    user_user_files.status_code('options', s.HTTP_200_OK)
    user_user_files.status_code('head', s.HTTP_200_OK)
    user_user_files.status_code('get', s.HTTP_200_OK)

    user_user_files.status_code('post', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_user_files.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_user_files.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_user_files.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)


  def test_file_contents(self):
    url = reverse('file_contents', kwargs={'pk': 1})
    file_contents = StatusCodeTest(self, url)
    file_contents.status_code('options', s.HTTP_401_UNAUTHORIZED)
    file_contents.status_code('get', s.HTTP_401_UNAUTHORIZED)

    file_contents.status_code('post', s.HTTP_401_UNAUTHORIZED)
    file_contents.status_code('put', s.HTTP_401_UNAUTHORIZED)
    file_contents.status_code('patch', s.HTTP_401_UNAUTHORIZED)
    file_contents.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    file_contents.status_code('head', s.HTTP_401_UNAUTHORIZED)


    user_file_contents = UserStatusCodeTest(self, url)
    FileModel.objects.create(name="file test 1",fk_user=user_file_contents.user)

    user_file_contents.status_code('options', s.HTTP_200_OK)
    user_file_contents.status_code('head', s.HTTP_200_OK)
    user_file_contents.status_code('get', s.HTTP_200_OK)

    user_file_contents.status_code('post', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_contents.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_contents.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_contents.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)


  def test_file_update_retrieve(self):
    url = reverse('file_update_retrieve', kwargs={'pk': 1})
    file_update = StatusCodeTest(self, url)
    file_update.status_code('options', s.HTTP_401_UNAUTHORIZED)
    file_update.status_code('get', s.HTTP_401_UNAUTHORIZED)
    file_update.status_code('put', s.HTTP_401_UNAUTHORIZED)
    file_update.status_code('patch', s.HTTP_401_UNAUTHORIZED)

    file_update.status_code('post', s.HTTP_401_UNAUTHORIZED)
    file_update.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    file_update.status_code('head', s.HTTP_401_UNAUTHORIZED)

    user_file_update = UserStatusCodeTest(self, url)
    FileModel.objects.create(name="file test 1",fk_user=user_file_update.user)
    user_file_update.status_code('options', s.HTTP_200_OK)
    user_file_update.status_code('head', s.HTTP_200_OK)
    user_file_update.status_code('get', s.HTTP_200_OK)
    user_file_update.status_code('patch', s.HTTP_200_OK)
    user_file_update.status_code('put', s.HTTP_400_BAD_REQUEST)

    user_file_update.status_code('post', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_update.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)


  def test_file_add(self):
    url = reverse('file_add')
    file_add = StatusCodeTest(self, url)
    file_add.status_code('post', s.HTTP_401_UNAUTHORIZED)
    file_add.status_code('options', s.HTTP_401_UNAUTHORIZED)

    file_add.status_code('get', s.HTTP_401_UNAUTHORIZED)
    file_add.status_code('put', s.HTTP_401_UNAUTHORIZED)
    file_add.status_code('patch', s.HTTP_401_UNAUTHORIZED)
    file_add.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    file_add.status_code('head', s.HTTP_401_UNAUTHORIZED)

    user_file_add = UserStatusCodeTest(self, url)
    user_file_add.status_code('post', s.HTTP_400_BAD_REQUEST)
    user_file_add.status_code('options', s.HTTP_200_OK)

    user_file_add.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_add.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_add.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_add.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_file_add.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)
