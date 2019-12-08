from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase
from files.models import FileModel
from tokens.tests.test_token_obtain import get_new_registered_user_tokens

"""
  path('user/',               UserFilesView.as_view(), name='user_files'),
  path('<int:pk>/contents/',  FilesContentsView.as_view(), name='file_contents'),
  path('<int:pk>/',           UpdateView.as_view(), name='file_update_retrieve'),
  path('',                    AddView.as_view(), name='file_add'),
"""


class CheckFileViews(APITestCase):
  file_index = 1
  test_maximum = 1

  def setUp(self):
    self.user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))

  def add_new_file(self):
    url = reverse('file_add')
    data = {'name': "file 1"}
    response = self.client.post(url, data, format='json')
    if response.status_code == 201:
      return response.json()
    
    data = {'name': "file 2, parent=1", 'fk_parent': fk_parent}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)


  def add_file_for_other_user(self):
    url = reverse('file_add')
    new_user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + new_user_tokens.get('access'))

    data = {'name': f"file {self.file_index} - other user"}
    response = self.client.post(url, data, format='json')
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)


  def test_add_parent_permissions(self):
    self.add_file_for_other_user()
    url = reverse('file_add')
    
    data = {'name': "test file add", 'fk_parent': 1}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['You do not have permissions on parent file.']}
    self.assertEqual(response.json(), err)
    
    data = {'name': "test file add", 'fk_parent': 100}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['Parent file does not exist.']}
    self.assertEqual(response.json(), err)


  def test_maximum_allowed_files(self, fk_parent=None):
    if self.test_maximum < 100:
      url = reverse('file_add')
      max_length = 9
      self.test_maximum += 1
      data = {'name': "test maximum", 'fk_parent': fk_parent}
      response = self.client.post(url, data, format='json')
      if response.status_code == 201:
        fk_parent = fk_parent or response.json().get('pk')
        children_total = FileModel.objects.filter(fk_parent=fk_parent).count()
        self.assertLessEqual(children_total, max_length)
        self.test_maximum_allowed_files(fk_parent)
      else:
        self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
        err = {'fk_parent': ['Parent file reached maximum allowed files.']}
        self.assertEqual(response.json(), err)

        children_total = FileModel.objects.filter(fk_parent=fk_parent).count()
        self.assertEqual(children_total, max_length)


  def test_add_others_files_as_parent(self):
    url = reverse('file_add')
    self.add_file_for_other_user()
    file_id = FileModel.objects.get(name="file 1 - other user").pk
    data = {'name': "file 1", 'fk_parent': file_id}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)


  def test_update_others_files_as_parent(self):
    url = reverse('file_add')
    self.add_file_for_other_user()
    file_id = FileModel.objects.get(name="file 1 - other user").pk
    data = {'name': "file 1", 'fk_parent': file_id}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)


  def test_normal_add_files(self):
    self.add_file_for_other_user()
    url = reverse('file_add')

    data = {'name': "file 1"}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)
    fk_parent = response.json().get('fk_parent')
    
    data = {'name': "file 2, parent=1", 'fk_parent': fk_parent}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_201_CREATED)
