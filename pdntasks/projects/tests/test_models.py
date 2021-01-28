import pytest

from ..models import Client, Project
from .factories import ClientFactory, ProjectFactory

pytestmark = pytest.mark.django_db


class TestClient:
    def test__str__(self):
        abbreviation = "ABC"
        client = ClientFactory(abbreviation=abbreviation)

        assert client.__str__() == abbreviation
        assert str(client) == abbreviation

    def test_abbreviation_caps(self):
        abbreviation = "abc"
        client = ClientFactory(abbreviation=abbreviation)

        assert client.abbreviation == abbreviation.upper()
        assert str(client) == abbreviation.upper()


class TestProject:
    def test__str__(self):
        abbreviation = "ABC"
        project = ProjectFactory(abbreviation=abbreviation)

        assert project.__str__() == abbreviation
        assert str(project) == abbreviation

    def test_abbreviation_caps(self):
        abbreviation = "abc"
        project = ProjectFactory(abbreviation=abbreviation)

        assert project.abbreviation == abbreviation.upper()
        assert str(project) == abbreviation.upper()
