from django.urls import reverse
from rest_framework import status as s
from rest_framework.test import APITestCase
from tokens.tests.test_urls import StatusCodeTest, UserStatusCodeTest
from files.models import FileModel
from contents.models import ContentModel

class CheckStatusCode(APITestCase):
  def test_content_update(self):
    url = reverse('content_update', kwargs={'pk': 1})
    content_update = StatusCodeTest(self, url)
    content_update.status_code('options', s.HTTP_401_UNAUTHORIZED)
    content_update.status_code('put', s.HTTP_401_UNAUTHORIZED)
    content_update.status_code('patch', s.HTTP_401_UNAUTHORIZED)

    content_update.status_code('get', s.HTTP_401_UNAUTHORIZED)
    content_update.status_code('post', s.HTTP_401_UNAUTHORIZED)
    content_update.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    content_update.status_code('head', s.HTTP_401_UNAUTHORIZED)

    user_content_update = UserStatusCodeTest(self, url)
    fk = FileModel.objects.create(name="1",fk_user=user_content_update.user)
    ContentModel.objects.create(text="content test 1", fk_file=fk)

    user_content_update.status_code('options', s.HTTP_200_OK)
    user_content_update.status_code('head', s.HTTP_200_OK)
    user_content_update.status_code('patch', s.HTTP_200_OK)
    user_content_update.status_code('get', s.HTTP_200_OK) # RetrieveUpdate
    user_content_update.status_code('put', s.HTTP_400_BAD_REQUEST)

    user_content_update.status_code('post', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_content_update.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)


  def test_content_add(self):
    url = reverse('content_add')
    content_add = StatusCodeTest(self, url)
    content_add.status_code('options', s.HTTP_401_UNAUTHORIZED)
    content_add.status_code('post', s.HTTP_401_UNAUTHORIZED)

    content_add.status_code('get', s.HTTP_401_UNAUTHORIZED)
    content_add.status_code('put', s.HTTP_401_UNAUTHORIZED)
    content_add.status_code('patch', s.HTTP_401_UNAUTHORIZED)
    content_add.status_code('delete', s.HTTP_401_UNAUTHORIZED)
    content_add.status_code('head', s.HTTP_401_UNAUTHORIZED)

    user_content_add = UserStatusCodeTest(self, url)
    user_content_add.status_code('options', s.HTTP_200_OK)
    user_content_add.status_code('post', s.HTTP_400_BAD_REQUEST)

    user_content_add.status_code('get', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_content_add.status_code('put', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_content_add.status_code('patch', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_content_add.status_code('delete', s.HTTP_405_METHOD_NOT_ALLOWED)
    user_content_add.status_code('head', s.HTTP_405_METHOD_NOT_ALLOWED)
