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
