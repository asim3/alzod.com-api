from datetime import timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def get_new_registered_user_tokens():
  url = reverse('register')
  data = {
    'username': "test_user",
    'password1': "fjdskfja",
    'password2': "fjdskfja"
  }
  client = APIClient()
  response = client.post(url, data, format='json')
  if response.status_code == 200:
    return response.json()
  return {}


class CheckToken(APITestCase):
  e_username = {'username': ['This field is required.']}
  e_password1 = {'password1': ['This field is required.']}
  e_similar = {'password2': ['The password is too similar to the username.']}
  e_common = {'password2': ['This password is too common.']}


  def test_registration_missing_username(self):
    url = reverse('register')
    data = {
      'password1': "fjdskfja",
      'password2': "fjdskfja"
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.json(), self.e_username)


  def test_registration_missing_password(self):
    url = reverse('register')
    data = {
      'username': "test_user",
      'password2': "fjdskfja"
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.json(), self.e_password1)


  def test_registration_password_common(self):
    url = reverse('register')
    data = {
      'username': "test_user",
      'password1': "abcdefgh",
      'password2': "abcdefgh"
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.json(), self.e_common)


  def test_registration_password_similar_to_username(self):
    url = reverse('register')
    data = {
      'username': "test_user",
      'password1': "test_user",
      'password2': "test_user"
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.json(), self.e_similar)


  def check_refresh_bad(self, refresh):
    url = reverse('token_refresh')
    data = {'refresh': refresh + "w"}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_401_UNAUTHORIZED)
    err = {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'}
    self.assertEqual(response.json(), err)


  def check_refresh(self, refresh):
    url = reverse('token_refresh')
    data = {'refresh': refresh}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    self.check_refresh_bad(refresh)


  def check_access(self, access):
    url = reverse('user_files')
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
    response = self.client.get(url, format='json')
    self.client.credentials()
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    response_check = {'count': 0, 'next': None, 'previous': None, 'results': []}
    self.assertEqual(response.json(), response_check)


  def test_register(self):
    data = get_new_registered_user_tokens()
    refresh = data.get('refresh')
    access = data.get('access')
    
    self.check_refresh(refresh)
    self.check_access(access)

    

  def test_login(self):
    url = reverse('token_obtain')
    User.objects.create_user("test_login", password="fjdskfja")
    data = {
      'username': "test_login",
      'password': "fjdskfja"
    }
    response = self.client.post(url, data, format='json')
    assert response.status_code == s.HTTP_200_OK
    
    json = response.json()
    refresh = json.get('refresh')
    access = json.get('access')
    
    self.check_refresh(refresh)
    self.check_access(access)


  def test_refresh(self):
    url = reverse('token_refresh')
    user = User.objects.create_user("test_old", password="fjdskfja")
    refresh = RefreshToken.for_user(user)
    
    # exp_days_left = 3.0 
    data = {'refresh': str(refresh)}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    self.assertIsNone(response.json().get('refresh'))

    # exp_days_left = 1.96 
    refresh.set_exp(lifetime=timedelta(hours=47))
    data = {'refresh': str(refresh)}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_200_OK)
    self.assertIsNotNone(response.json().get('refresh'))

    # exp_days_left = 0.0
    refresh.set_exp(lifetime=-timedelta(seconds=1))
    data = {'refresh': str(refresh)}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, s.HTTP_401_UNAUTHORIZED)