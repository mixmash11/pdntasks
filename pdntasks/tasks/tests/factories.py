import factory
import factory.fuzzy

from ...projects.tests.factories import ProjectFactory

from ..models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("bs")
    info = factory.Faker("paragraphs")
    assigned_to = None
    project = factory.SubFactory(ProjectFactory)
    parent_task = None

    class Meta:
        model = Task
