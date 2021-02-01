import factory
import factory.fuzzy

from ..models import Client, Project


class ClientFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    abbreviation = factory.fuzzy.FuzzyText(length=3)
    info = factory.Faker("paragraphs")

    class Meta:
        model = Client


class ProjectFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("bs")
    abbreviation = factory.fuzzy.FuzzyText(length=3)
    info = factory.Faker("paragraphs")
    if factory.Faker("pybool"):
        client = factory.SubFactory(ClientFactory)
    else:
        client = None

    class Meta:
        model = Project
