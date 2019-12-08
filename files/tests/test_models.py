from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status as s
from rest_framework.test import APITestCase
from files.models import FileModel


class CheckFileModel(APITestCase):
  def setUp(self):
    user_1 = User.objects.create_user("file_check_1", password="Aa59f2342")
    user_2 = User.objects.create_user("file_check_2", password="Aa59f2342")
    user_3 = User.objects.create_user("file_check_3", password="Aa59f2342")

    file_1 = FileModel.objects.create(name="file_check_1", fk_user=user_1)
    file_2 = FileModel.objects.create(name="file_check_2", fk_user=user_2)
    file_3 = FileModel.objects.create(name="file_check_3", fk_user=user_3)

    file_2_1 = FileModel.objects.create(fk_parent=file_2, name="file_2_1", fk_user=user_2)
    file_2_2 = FileModel.objects.create(fk_parent=file_2, name="file_2_2", fk_user=user_2)
    file_2_3 = FileModel.objects.create(fk_parent=file_2, name="file_2_3", fk_user=user_2)

    file_2_1_1 = FileModel.objects.create(fk_parent=file_2_1, name="file_2_1_1", fk_user=user_2)


  def test_parents_ids(self):
    file_2 = FileModel.objects.get(name="file_check_2")
    self.assertEqual(file_2.parents_ids(), None)
    file_2_1 = FileModel.objects.get(name="file_2_1")
    self.assertEqual(file_2_1.parents_ids(), [file_2.id])
    file_2_1_1 = FileModel.objects.get(name="file_2_1_1")
    self.assertEqual(file_2_1_1.parents_ids(), [file_2.id, file_2_1.id])


  # def test_parents_as_list(self):
  #   pass

  # def test_user_as_dict(self):
  #   user = User.objects.filter(username="file_check_1")

  def test_children_as_list(self):
    file_2 = FileModel.objects.get(name="file_check_2")
    children = [
      {'id': 4, 'name': 'file_2_1', 'photo': 'http://localhost:8000/', 'is_public': False}, 
      {'id': 5, 'name': 'file_2_2', 'photo': 'http://localhost:8000/', 'is_public': False}, 
      {'id': 6, 'name': 'file_2_3', 'photo': 'http://localhost:8000/', 'is_public': False}
    ]
    self.assertEqual(file_2.children_as_list(), children)