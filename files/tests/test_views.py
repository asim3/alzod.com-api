from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase
from files.models import FileModel
from tokens.tests.test_token_obtain import get_new_registered_user_tokens


class CheckFileViews(APITestCase):
  test_number = 1
  maximum_loop = 100

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
    new_user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + new_user_tokens.get('access'))
    file_U = self.add_new_file(parent)
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))
    return file_U

  def get_file_data(self, pk):
    self.assertIsNotNone(pk)
    url = reverse('file_update_retrieve', kwargs={'pk': pk})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    return response.json()
    
  def get_children_total(self, pk):
    self.assertIsNotNone(pk)
    parent_data = self.get_file_data(pk=pk)
    return len(parent_data.get('file_children'))


  def test_add_parent_bad(self):
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
    max_length = 9
    self.test_number += 1
    if self.test_number <= self.maximum_loop:
      self.assertLess(self.test_number, self.maximum_loop)
      url = reverse('file_add')
      data = {'name': "test maximum", 'fk_parent': fk_parent}
      response = self.client.post(url, data, format='json')
      if response.status_code == 201:
        fk_parent = fk_parent or response.json().get('pk')
        children_total = self.get_children_total(pk=fk_parent)
        self.assertLessEqual(children_total, max_length)
        self.test_maximum_allowed_files(fk_parent)
      else:
        self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
        err = {'fk_parent': ['Parent file reached maximum allowed files.']}
        self.assertEqual(response.json(), err)

        children_total = self.get_children_total(pk=fk_parent)
        self.assertEqual(children_total, max_length)


  def test_add_others_files_as_parent(self):
    url = reverse('file_add')
    other_file = self.add_file_for_other_user()
    data = {'name': "file 1", 'fk_parent': other_file.get('pk')}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['You do not have permissions on parent file.']}
    self.assertEqual(response.json(), err)


  def test_add_files(self):
    other_file = self.add_file_for_other_user()
    user_file_1 = self.add_new_file()
    user_file_2 = self.add_new_file(parent=user_file_1.get('pk'))
    user_file_3 = self.add_new_file(parent=user_file_2.get('pk'))
    user_file_4 = self.add_new_file(parent=user_file_3.get('pk'))
    user_file_5 = self.add_new_file(parent=user_file_4.get('pk'))
    for i in range(4):
      self.add_new_file(parent=user_file_5.get('pk'))
    child_file = self.add_new_file(parent=user_file_5.get('pk'))
    data_check = [
      {'order': 4, 'id': 3, 'name': 'file 1'},
      {'order': 3, 'id': 4, 'name': 'file 1'},
      {'order': 2, 'id': 5, 'name': 'file 1'},
      {'order': 1, 'id': 6, 'name': 'file 1'}
    ]
    self.assertEqual(child_file.get('file_parents'), data_check)

    self.assertEqual(self.get_children_total(pk=user_file_1.get('pk')), 1)
    self.assertEqual(self.get_children_total(pk=user_file_2.get('pk')), 1)
    self.assertEqual(self.get_children_total(pk=user_file_3.get('pk')), 1)
    self.assertEqual(self.get_children_total(pk=user_file_4.get('pk')), 1)
    self.assertEqual(self.get_children_total(pk=user_file_5.get('pk')), 5)


  def test_update(self):
    user_file_1 = self.add_new_file()
    user_file_2 = self.add_new_file()
    url = reverse('file_update_retrieve', kwargs={'pk': user_file_1.get('pk')})

    data = {'fk_parent': user_file_2.get('pk')}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'name': ['This field is required.']}
    self.assertEqual(response.json(), err)

    data = {'name': "update file 52521", 'fk_parent': user_file_2.get('pk')}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    err = {'name': ['This field is required.']}
    self.assertEqual(response.json().get('name'), "update file 52521")

    data = {'name': "update patch file 9756"}
    response = self.client.patch(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    self.assertEqual(response.json().get('name'), "update patch file 9756")


  def test_update_others_files_as_parent(self):
    other_file = self.add_file_for_other_user()
    user_file = self.add_new_file()
    url = reverse('file_update_retrieve', kwargs={'pk': user_file.get('pk')})

    data = {'fk_parent': other_file.get('pk')}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['You do not have permissions on parent file.']}
    self.assertEqual(response.json(), err)

    data = {'fk_parent': other_file.get('pk')}
    response = self.client.patch(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['You do not have permissions on parent file.']}
    self.assertEqual(response.json(), err)


  def test_update_to_self_parent(self):
    user_file_1 = self.add_new_file()
    user_file_2 = self.add_new_file(parent=user_file_1.get('pk'))
    user_file_3 = self.add_new_file(parent=user_file_2.get('pk'))
    user_file_4 = self.add_new_file(parent=user_file_3.get('pk'))

    url = reverse('file_update_retrieve', kwargs={'pk': user_file_1.get('pk')})

    data = {'fk_parent': user_file_1.get('pk'), 'name': "put 543"}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['File cannot be parent of himself.']}
    self.assertEqual(response.json(), err)

    data = {'fk_parent': user_file_1.get('pk')}
    response = self.client.patch(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['File cannot be parent of himself.']}
    self.assertEqual(response.json(), err)

    url = reverse('file_update_retrieve', kwargs={'pk': user_file_4.get('pk')})

    data = {'fk_parent': user_file_4.get('pk'), 'name': "put 543"}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['File cannot be parent of himself.']}
    self.assertEqual(response.json(), err)

    data = {'fk_parent': user_file_4.get('pk')}
    response = self.client.patch(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    err = {'fk_parent': ['File cannot be parent of himself.']}
    self.assertEqual(response.json(), err)


  def test_user_files(self):
    user_file_1 = self.add_new_file()
    user_file_2 = self.add_new_file()
    user_file_3 = self.add_new_file()
    self.add_new_file(parent=user_file_3.get('pk'))
    self.add_new_file(parent=user_file_3.get('pk'))
    
    response = self.client.get(reverse('user_files'), format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    self.assertEqual(response.json().get('count'), 3)