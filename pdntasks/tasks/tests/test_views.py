import pytest
from pytest_django.asserts import assertContains
from slugify import slugify

from .factories import TaskFactory
from ..models import Task
from ..views import TaskListView, TaskDetailView

from django.urls import reverse

from ...projects.tests.factories import ProjectFactory
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def task():
    return TaskFactory()


@pytest.fixture
def project():
    return ProjectFactory()


class TestTask:
    def test_task_list_view(self, user, rf):
        request = rf.get(reverse("tasks:task_list"))
        request.user = user
        response = TaskListView.as_view()(request)
        assertContains(response, "Task List")

    def test_task_list_view_contains_2_tasks(self, user, rf):
        project_abb = "ABC"

        project = ProjectFactory(abbreviation="ABC")

        task_1 = TaskFactory(project=project)
        task_2 = TaskFactory(project=project)

        task_slug = slugify(project_abb)

        request = rf.get(reverse("tasks:task_list"))
        request.user = user
        response = TaskListView.as_view()(request)
        assertContains(response, f"{task_slug}")
        assertContains(response, f"{task_slug}-2")

    def test_task_detail_view(self, user, rf, task):
        url = reverse("tasks:task_detail", kwargs={"slug": task.slug})
        request = rf.get(url)
        request.user = user
        callable_obj = TaskDetailView.as_view()
        response = callable_obj(request, slug=task.slug)
        assertContains(response, task.name)

    def test_get_absolute_url(self):
        task = TaskFactory()
        url = task.get_absolute_url()
        assert url == f"/tasks/{task.slug}/"

    def test_task_create_view(self, client, user):
        url = reverse("tasks:task_add")
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 200

    def test_task_create_view_has_correct_title(self, client, user):
        url = reverse("tasks:task_add")
        client.force_login(user)
        response = client.get(url)
        assertContains(response, "Add Task")

    def test_task_create_form_valid(self, client, user, project):
        form_data = {
            "name": "Do the Thing",
            "status": "open",
            "assigned_to": "",
            "parent_task": "",
            "info": "Make the stuff",
            "project": project.pk,
        }
        url = reverse("tasks:task_add")
        client.force_login(user)
        response = client.post(url, form_data)

        task = Task.objects.get()

        assert task.name == form_data["name"]
        assert task.info == form_data["info"]

    def test_task_update_view_has_correct_title(self, client, user, task):
        url = reverse("tasks:task_update", kwargs={"slug": task.slug})
        client.force_login(user)
        response = client.get(url)
        assertContains(response, "Update Task")

    def test_task_update(self, client, user, task):
        test_name = "Do Something Else"
        form_data = {
            "name": test_name,
            "status": task.status,
            "assigned_to": "",
            "parent_task": "",
            "info": task.info,
            "project": task.project.pk,
        }
        url = reverse("tasks:task_update", kwargs={"slug": task.slug})
        client.force_login(user)
        response = client.post(url, form_data)
        task.refresh_from_db()
        assert task.name == test_name
