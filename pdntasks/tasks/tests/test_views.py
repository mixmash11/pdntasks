import pytest
from pytest_django.asserts import assertContains
from slugify import slugify

from .factories import TaskFactory
from ..views import TaskListView, TaskDetailView

from django.urls import reverse

from ...projects.tests.factories import ProjectFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def task():
    return TaskFactory()


class TestTask:
    def test_task_list_view(self, rf):
        request = rf.get(reverse("tasks:task_list"))
        response = TaskListView.as_view()(request)
        assertContains(response, "Task List")

    def test_task_list_view_contains_2_tasks(self, rf):
        project_abb = "ABC"

        project = ProjectFactory(abbreviation="ABC")

        task_1 = TaskFactory(project=project)
        task_2 = TaskFactory(project=project)

        task_slug = slugify(project_abb)

        request = rf.get(reverse("tasks:task_list"))
        response = TaskListView.as_view()(request)
        assertContains(response, f"{task_slug}")
        assertContains(response, f"{task_slug}-2")

    def test_task_detail_view(self, rf, task):
        url = reverse("tasks:task_detail", kwargs={"slug": task.slug})
        request = rf.get(url)
        callable_obj = TaskDetailView.as_view()
        response = callable_obj(request, slug=task.slug)
        assertContains(response, task.name)
