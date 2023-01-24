from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import ToDoList, Task

class ViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser("test_superuser")
        self.client.force_login(self.user)

        self.todo_list = ToDoList.objects.create(title="test list", user=self.user)

    def test_root_redirects(self):
        # arrange
        url = "/"

        # act
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, 302)

    def test_root_redirects_new_user_to__show_lists(self):
        # arrange
        url = "/"
        new_user = get_user_model().objects.create()
        expected_path = reverse("show-lists")
        self.client.force_login(new_user)

        # act
        response = self.client.get(url, follow=True)

        # assert
        last_redirect_path, last_redirect_status = response.redirect_chain[-1]
        self.assertEqual(expected_path, last_redirect_path)