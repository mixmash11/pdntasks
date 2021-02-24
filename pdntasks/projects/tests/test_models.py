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

    def test_get_absolute_url(self):
        client = ClientFactory()
        url = client.get_absolute_url()
        assert url == f"/project_management/clients/{client.slug}/"


class TestProject:
    def test__str__(self):
        abbreviation = "abc"
        project = ProjectFactory(abbreviation=abbreviation)

        assert project.__str__() == abbreviation
        assert str(project) == abbreviation

    def test_abbreviation_caps(self):
        abbreviation = "abc"
        project = ProjectFactory(abbreviation=abbreviation)

        assert project.abbreviation == abbreviation.upper()
        assert str(project) == abbreviation.upper()

    def test_get_absolute_url(self):
        project = ProjectFactory()
        url = project.get_absolute_url()
        assert url == f"/project_management/projects/{project.slug}/"
