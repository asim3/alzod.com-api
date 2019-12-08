from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase
from files.models import FileModel
from tokens.tests.test_token_obtain import get_new_registered_user_tokens


class CheckContentsViews(APITestCase):
  test_maximum = 1

  def setUp(self):
    self.user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))

  def add_new_file(self, parent=None):
    url = reverse('file_add')
    data = {'name': "file 1", 'fk_parent': parent}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)
    return response.json()

  def add_file_for_other_user(self, parent=None):
    url = reverse('file_add')
    data = {'name': "file - other user", 'fk_parent': parent}
    new_user_tokens = get_new_registered_user_tokens()

    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + new_user_tokens.get('access'))
    response = self.client.post(url, data, format='json')
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)
    return response.json()

  def get_file_data(self, pk=None):
    self.assertIsNotNone(pk)
    url = reverse('file_update_retrieve', kwargs={'pk': pk})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    return response.json()