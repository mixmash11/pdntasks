import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from ..models import Client, Project
from ..views import ClientListView, ProjectListView, ClientDetailView, ProjectDetailView
from .factories import ClientFactory, ProjectFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return ClientFactory()


@pytest.fixture
def project():
    return ProjectFactory()


class TestClientViews:
    def test_client_list_view(self, rf):
        request = rf.get(reverse("projects:client_list"))
        response = ClientListView.as_view()(request)
        assertContains(response, "Client List")

    def test_client_list_view_contains_2_members(self, rf):

        client1 = ClientFactory()
        client2 = ClientFactory()
        request = rf.get(reverse("projects:client_list"))
        response = ClientListView.as_view()(request)
        assertContains(response, client1.abbreviation)
        assertContains(response, client2.abbreviation)

    def test_client_detail_view(self, rf, client):
        url = reverse("projects:client_detail", kwargs={"slug": client.slug})
        request = rf.get(url)
        callable_obj = ClientDetailView.as_view()
        response = callable_obj(request, slug=client.slug)
        assertContains(response, client.abbreviation)


class TestProjectViews:
    def test_project_list_view(self, rf):
        request = rf.get(reverse("projects:project_list"))
        response = ProjectListView.as_view()(request)
        assertContains(response, "Project List")

    def test_project_list_view_contains_2_members(self, rf):

        project1 = ProjectFactory()
        project2 = ProjectFactory()
        request = rf.get(reverse("projects:project_list"))
        response = ProjectListView.as_view()(request)
        assertContains(response, project1.abbreviation)
        assertContains(response, project2.abbreviation)

    def test_project_detail_view(self, rf, project):
        url = reverse("projects:project_detail", kwargs={"slug": project.slug})
        request = rf.get(url)
        callable_obj = ProjectDetailView.as_view()
        response = callable_obj(request, slug=project.slug)
        assertContains(response, project.abbreviation)
