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
        url = reverse("root")

        # act
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, 302)

    def test_root_redirects_new_user_to__show_lists(self):
        # arrange
        url = reverse("root")
        new_user = get_user_model().objects.create()
        expected_path = reverse("show-lists")
        self.client.force_login(new_user)

        # act
        response = self.client.get(url, follow=True)

        # assert
        last_redirect_url, last_redirect_status = response.redirect_chain[-1]
        self.assertEqual(expected_path, last_redirect_url)

    def test_root_redirects_anonymous_user_to__login(self):
        # arrange
        url = reverse("root")
        expected_path = reverse("login")

        # act
        response = Client().get(url, follow=True)  # new client to not force login

        # assert
        last_redirect_url, last_redirect_status = response.redirect_chain[-1]
        url_without_qs = last_redirect_url.split("?")[0]
        self.assertEqual(expected_path, url_without_qs)

    def test_root_redirects_user_with_list_to__list_detail(self):
        # arrange
        url = reverse("root")
        expected_path = reverse("list-detail", kwargs={"slug": self.todo_list.slug})

        # act
        response = self.client.get(url, follow=True)

        # assert
        last_redirect_url, last_redirect_status = response.redirect_chain[-1]
        self.assertEqual(expected_path, last_redirect_url)

    def test_root_redirects_user_with_list_to__most_recent_list_detail(self):
        # arrange
        url = reverse("root")
        new_list = ToDoList.objects.create(title="newest list", user=self.user)
        expected_path = reverse("list-detail", kwargs={"slug": new_list.slug})

        # act
        response = self.client.get(url, follow=True)

        # assert
        last_redirect_url, last_redirect_status = response.redirect_chain[-1]
        self.assertEqual(expected_path, last_redirect_url)

    def test_root_redirects_user_with_no_lists_to__page_saying_you_have_no_lists(self):
        # arrange
        url = reverse("root")
        self.todo_list.delete()

        # act
        response = self.client.get(url, follow=True)

        # assert
        self.assertContains(response, "You have no todo lists.")

    def test_show_lists_view(self):
        # arrange
        url = reverse("show-lists")

        # act
        response = self.client.get(url)

        # assert
        self.assertContains(response, "Todo Lists")

    def test_show_lists_view__displays_list_title(self):
        # arrange
        url = reverse("show-lists")
        expected_title = "expected title"
        self.todo_list.title = expected_title
        self.todo_list.save()

        # act
        response = self.client.get(url)

        # assert
        self.assertContains(response, expected_title)

    def test_create_list_view(self):
        # arrange
        url = reverse("list-add")
        expected_title = "added list"

        # act
        self.client.post(url, {"title": expected_title})

        # assert
        self.assertTrue(ToDoList.objects.filter(title=expected_title))

    def test_create_task_view(self):
        # arrange
        url = reverse("task-add", kwargs={"slug": self.todo_list.slug})
        expected_task_name = "new task name"

        # act
        self.client.post(url, {"name": expected_task_name})

        # assert
        self.assertTrue(Task.objects.filter(name=expected_task_name))

    def test_list_toggle_active_view__changes_state_from_true_to_false(self):
        # arrange
        url = reverse("list-toggle-active", kwargs={"slug": self.todo_list.slug})
        expected_active = False
        self.todo_list.active = not expected_active  # make sure we're not starting off with the expected value
        self.todo_list.save()

        # act
        self.client.get(url)

        # assert
        self.assertEqual(ToDoList.objects.get(id=self.todo_list.id).active, expected_active)

    def test_list_toggle_active_view__changes_state_from_false_to_true(self):
        # arrange
        url = reverse("list-toggle-active", kwargs={"slug": self.todo_list.slug})
        expected_active = True
        self.todo_list.active = not expected_active  # make sure we're not starting off with the expected value
        self.todo_list.save()

        # act
        self.client.get(url)

        # assert
        self.assertEqual(ToDoList.objects.get(id=self.todo_list.id).active, expected_active)

    def test_list_delete_view__deletes_list(self):
        # arrange
        url = reverse("list-delete", kwargs={"slug": self.todo_list.slug})

        # act
        self.client.post(url)

        # assert
        self.assertEqual(ToDoList.objects.filter(slug=self.todo_list.slug).count(), 0)

    def test_list_update_view__updates_list(self):
        # arrange
        url = reverse("list-update", kwargs={"slug": self.todo_list.slug})
        expected_new_title = "new test list new!"

        # act
        self.client.post(url, {"title": expected_new_title})

        # assert
        self.assertNotEqual(ToDoList.objects.filter(title=expected_new_title).count(), 0)

    def test_list_detail__displays_list_title(self):
        # arrange
        url = reverse("list-detail", kwargs={"slug": self.todo_list.slug})

        # act
        response = self.client.get(url)

        # assert
        self.assertContains(response, self.todo_list.title)

    def test_task_toggle_completed_view__changes_state_of_task_from_false_to_true(self):
        # arrange
        expected_completed_state = True
        test_task = Task.objects.create(name="test task",
                                        todo_list=self.todo_list,
                                        completed=not expected_completed_state)
        url = reverse("task-toggle-complete", kwargs={"pk": test_task.id})

        # act
        self.client.get(url)

        # assert
        self.assertEqual(Task.objects.get(id=test_task.id).completed, expected_completed_state)

    def test_task_toggle_completed_view__changes_state_of_task_from_true_to_false(self):
        # arrange
        expected_completed_state = False
        test_task = Task.objects.create(name="test task",
                                        todo_list=self.todo_list,
                                        completed=not expected_completed_state)
        url = reverse("task-toggle-complete", kwargs={"pk": test_task.id})

        # act
        self.client.get(url)

        # assert
        self.assertEqual(Task.objects.get(id=test_task.id).completed, expected_completed_state)

    def test_task_update__changes_task_description(self):
        # arrange
        expected_description = "this is the new description"
        test_task = Task.objects.create(name="test task", todo_list=self.todo_list)
        url = reverse("task-update", kwargs={"pk": test_task.id})

        # act
        self.client.post(url, {"name": test_task.name, "description": expected_description})

        # asseert
        self.assertEqual(Task.objects.get(id=test_task.id).description, expected_description)