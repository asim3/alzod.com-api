from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase
from files.models import FileModel
from tokens.tests.test_token_obtain import get_new_registered_user_tokens

print('\n\n\n', 111, '\n')


class CheckContentsViews(APITestCase):
  test_number = 1
  maximum_loop = 100

  def setUp(self):
    self.user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))

  def add_new_file(self, parent=None):
    url = reverse('file_add')
    data = {'name': "file " + str(datetime.now())[-5:], 'fk_parent': parent}
    response = self.client.post(url, data, format='json')
    data = response.json()
    data['status_code'] = response.status_code
    return data

  def get_file_data(self, pk):
    self.assertIsNotNone(pk)
    url = reverse('file_update_retrieve', kwargs={'pk': pk})
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    return response.json()

  ############
  # contents #
  ############
  def add_new_content(self, fk_file):
    self.assertIsNotNone(fk_file)
    url = reverse('content_add')
    content_text = "add content " + str(datetime.now())[-5:]
    data = {'content_type': "t", 'text': content_text, 'fk_file': fk_file}
    response = self.client.post(url, data, format='json')
    data = response.json()
    data['status_code'] = response.status_code
    return data

  def get_content_data(self, pk):
    self.assertIsNotNone(pk)
    url = reverse('content_update', kwargs={'pk': pk})
    response = self.client.get(url, format='json')
    data = response.json()
    data['status_code'] = response.status_code
    return data

  def update_content(self, pk, data={}):
    self.assertIsNotNone(pk)
    url = reverse('content_update', kwargs={'pk': pk})
    response = self.client.put(url, data, format='json')
    response_data = response.json()
    response_data['status_code'] = response.status_code
    return response_data

  def patch_content(self, pk, data={}):
    self.assertIsNotNone(pk)
    url = reverse('content_update', kwargs={'pk': pk})
    response = self.client.patch(url, data, format='json')
    response_data = response.json()
    response_data['status_code'] = response.status_code
    return response_data

  def get_file_content(self, pk):
    self.assertIsNotNone(pk)
    url = reverse('file_contents', kwargs={'pk': pk})
    response = self.client.get(url, format='json')
    data = response.json()
    data['status_code'] = response.status_code
    return data

  def add_contents_for_other_user(self):
    new_user_tokens = get_new_registered_user_tokens()
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + new_user_tokens.get('access'))

    file_1 = self.add_new_file()
    content_1 = self.add_new_content(file_1.get('pk'))
    self.assertEqual(content_1.get('status_code'), s.HTTP_201_CREATED)
    content_2 = self.add_new_content(file_1.get('pk'))
    self.assertEqual(content_1.get('status_code'), s.HTTP_201_CREATED)
    data = self.get_file_content(file_1.get('pk'))
    data['pk'] = file_1.get('pk')

    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.user_tokens.get('access'))
    
    self.assertEqual(file_1.get('status_code'), s.HTTP_201_CREATED)
    self.assertEqual(content_1.get('status_code'), s.HTTP_201_CREATED)
    self.assertEqual(content_2.get('status_code'), s.HTTP_201_CREATED)
    return data

  #########
  # tests #
  #########
  def test_add_content_required(self):
    file_1 = self.add_new_file()
    url = reverse('content_add')

    data = {}
    err = {
      'fk_file': ['This field is required.'],
      'content_type': ['This field is required.'],
      'text': ['This field is required.']
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.json(), err)

    data = {'content_type': "   ", 'text': "    ", 'fk_file': file_1.get('pk')}
    err = {
      'content_type': ['This field may not be blank.'],
      'text': ['This field may not be blank.']
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.json(), err)


  def test_add_content_bad(self):
    file_U = self.add_contents_for_other_user()
    file_UT = self.add_contents_for_other_user()
    file_1 = self.add_new_file()

    content_1 = self.add_new_content(file_U.get('pk'))
    content_1_err = {
      'fk_parent': ['You do not have permissions on parent file.'],
      'status_code': 400
    }
    self.assertEqual(content_1.get('status_code'), s.HTTP_400_BAD_REQUEST)
    self.assertEqual(content_1, content_1_err)

    content_2 = self.add_new_content(385)
    content_2_err = {'fk_file': ['File does not exist.'], 'status_code': 400}
    self.assertEqual(content_2.get('status_code'), s.HTTP_400_BAD_REQUEST)
    self.assertEqual(content_2, content_2_err)

    content_3 = self.add_new_content("385")
    content_3_err = {'fk_file': ['Invalid file id..'], 'status_code': 400}
    self.assertEqual(content_3.get('status_code'), s.HTTP_400_BAD_REQUEST)
    self.assertEqual(content_3, content_3_err)


  # max content not implemented yet
  def test_maximum_allowed_content(self, fk_parent=None):
    max_length = 90
    self.test_number += 1
    if self.test_number <= self.maximum_loop and 1==2:
      self.assertLess(self.test_number, self.maximum_loop)
      if fk_parent is None:
        parent = self.add_new_file()
        self.test_maximum_allowed_content(parent.get('pk'))
      else:
        content = self.add_new_content(fk_parent)
        if content.get('status_code') == 201:
          total_content = self.get_file_content(fk_parent)
          self.assertLess(total_content.get('count'), max_length, "max content")
          self.test_maximum_allowed_content(fk_parent)
        else:
          self.assertEqual(content.get('status_code'), s.HTTP_400_BAD_REQUEST)


  def test_add_content(self):
    file_U_1 = self.add_contents_for_other_user()
    file_U_2 = self.add_contents_for_other_user()
    file_1 = self.add_new_file()

    content_error_1 = self.add_new_content(file_U_1.get('pk'))
    self.assertEqual(content_error_1.get('status_code'), s.HTTP_400_BAD_REQUEST)
    content_error_2 = self.add_new_content(file_U_2.get('pk'))
    self.assertEqual(content_error_2.get('status_code'), s.HTTP_400_BAD_REQUEST)

    file_contents = []
    for i in range(5):
      content = self.add_new_content(file_1.get('pk'))
      self.assertEqual(content.get('status_code'), s.HTTP_201_CREATED)
      del content['status_code']
      file_contents.append(content)

    file_1_contents = self.get_file_content(file_1.get('pk')).get('results')
    self.assertEqual(file_1_contents, file_contents)


  def test_show_content_bad(self):
    file_U_1 = self.add_contents_for_other_user()
    file_1 = self.add_new_file()
    content_1 = self.add_new_content(file_1.get('pk'))

    content_err = self.get_file_content(file_U_1.get('pk'))
    self.assertEqual(content_err.get('status_code'), s.HTTP_404_NOT_FOUND)
    
    content_err = self.get_content_data(1)
    self.assertEqual(content_err.get('status_code'), s.HTTP_404_NOT_FOUND)
    
    content_err = self.get_content_data(6187)
    self.assertEqual(content_err.get('status_code'), s.HTTP_404_NOT_FOUND)
    
    content_err = self.get_content_data(3)
    self.assertEqual(content_err.get('status_code'), s.HTTP_404_NOT_FOUND)
    
    content_err = self.get_content_data(2)
    self.assertEqual(content_err.get('status_code'), s.HTTP_404_NOT_FOUND)


  def test_update_content(self):
    file_U_1 = self.add_contents_for_other_user()
    file_U_2 = self.add_contents_for_other_user()
    file_1 = self.add_new_file()

    file_contents = []
    for i in range(5):
      content = self.add_new_content(file_1.get('pk'))
      self.assertEqual(content.get('status_code'), s.HTTP_201_CREATED)

      del content['status_code']
      file_contents.append(content)

    file_1_contents = self.get_file_content(file_1.get('pk')).get('results')
    self.assertEqual(file_1_contents, file_contents)


  def test_update_content_bad(self):
    file_U_1 = self.add_contents_for_other_user()
    file_U_2 = self.add_contents_for_other_user()
    file_1 = self.add_new_file()
    content_1 = self.add_new_content(file_1.get('pk'))
    
    err_permissions = {
      'fk_parent': ['You do not have permissions on parent file.'],
      'status_code': 400
    }


    # content_err = self.get_content_data(file_1.get('pk'))
    # print('\n\n\n', content_err, '\n')

    # content_err = self.get_content_data(content_1.get('pk'))
    # print('\n\n\n', content_err, '\n')
    # self.assertEqual(content_err.get('status_code'), s.HTTP_400_BAD_REQUEST)
    # self.assertEqual(content_err, err_permissions)

    # data = {'content_type': "t", 'text': "update 123321", 'fk_file': file_1.get('pk')}
    # content_err = self.update_content(file_1.get('pk'), data)
    # self.assertEqual(content_err.get('status_code'), s.HTTP_400_BAD_REQUEST)
    # print('\n\n\n', content_err, '\n')
    # err = {'fk_parent': ['You do not have permissions on parent file.'], 'status_code': 400}
    # self.assertEqual(content_err, err)

    # data = {'content_type': "t", 'text': "update 123321", 'fk_file': 9999}
    # content_err = self.update_content(file_1.get('pk'), data)
    # self.assertEqual(content_err.get('status_code'), s.HTTP_400_BAD_REQUEST)
    # print('\n\n\n', content_err, '\n')
    # err = {'fk_parent': ['You do not have permissions on parent file.'], 'status_code': 400}
    # self.assertEqual(content_err, err)

    # data = {'fk_file': file_1.get('pk')}
    # content_err = self.patch_content(file_1.get('pk'), data)
    # self.assertEqual(content_err.get('status_code'), s.HTTP_400_BAD_REQUEST)
    # print('\n\n\n', content_err, '\n')
    # err = {'fk_parent': ['You do not have permissions on parent file.'], 'status_code': 400}
    # self.assertEqual(content_err, err)

    # data = {'fk_file': 9999}
    # content_err = self.patch_content(file_1.get('pk'), data)
    # self.assertEqual(content_err.get('status_code'), s.HTTP_400_BAD_REQUEST)
    # print('\n\n\n', content_err, '\n')
    # err = {'fk_parent': ['You do not have permissions on parent file.'], 'status_code': 400}
    # self.assertEqual(content_err, err)
