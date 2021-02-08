import factory
import factory.fuzzy

from ...projects.tests.factories import ProjectFactory

from ..models import Task, Note
from ...users.tests.factories import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("bs")
    info = factory.Faker("paragraphs")
    assigned_to = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    parent_task = None

    class Meta:
        model = Task


class NoteFactory(factory.django.DjangoModelFactory):

    task = factory.SubFactory(TaskFactory)
    text = factory.Faker("paragraphs")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Note
