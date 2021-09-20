from datetime import date, timedelta

import pytest
from autoslug.utils import slugify

from ..models import Task
from ...projects.tests.factories import ProjectFactory

from .factories import TaskFactory

pytestmark = pytest.mark.django_db


class TestTask:
    def test__str__(self):
        project_abb = "ABC"
        project = ProjectFactory(abbreviation="ABC")

        task = TaskFactory(project=project)

        assert task.__str__() == slugify(project_abb)
        assert str(task) == slugify(project_abb)

    def test_incrementing_slug(self):
        project_abb = "ABC"

        project = ProjectFactory(abbreviation="ABC")

        task_1 = TaskFactory(project=project)
        task_2 = TaskFactory(project=project)

        task_slug = slugify(project_abb)

        assert task_1.__str__() == f"{task_slug}"
        assert task_2.__str__() == f"{task_slug}-2"

    def test_repeat_task_created(self):

        task = TaskFactory(repeats="daily")

        assert Task.objects.count() == 1

        task.status = "complete"
        task.save()

        assert Task.objects.count() == 2

    def test_repeat_task_not_created(self):

        task = TaskFactory(repeats="daily")

        assert Task.objects.count() == 1

        task.status = "inactive"
        task.save()

        assert Task.objects.count() == 1

    def test_repeat_task_due_date(self):
        task = TaskFactory(repeats="daily")
        task.status = "complete"
        task.save()

        new_task = Task.objects.last()

        assert new_task.date_due == date.today() + timedelta(1)
