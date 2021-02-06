import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse

from ..views import ClientListView, ProjectListView, ClientDetailView, ProjectDetailView
from ..models import Client, Project
from .factories import ClientFactory, ProjectFactory
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user():
    return UserFactory()


@pytest.fixture
def client_instance():
    return ClientFactory()


@pytest.fixture
def project():
    return ProjectFactory()


class TestClientViews:
    def test_client_list_view(self, user, rf):

        request = rf.get(reverse("projects:client_list"))
        request.user = user
        response = ClientListView.as_view()(request)
        assertContains(response, "Client List")

    def test_client_list_view_contains_2_members(self, user, rf):

        client1 = ClientFactory()
        client2 = ClientFactory()
        request = rf.get(reverse("projects:client_list"))
        request.user = user
        response = ClientListView.as_view()(request)
        assertContains(response, client1.abbreviation)
        assertContains(response, client2.abbreviation)

    def test_client_detail_view(self, user, rf, client_instance):

        url = reverse("projects:client_detail", kwargs={"slug": client_instance.slug})
        request = rf.get(url)
        request.user = user
        callable_obj = ClientDetailView.as_view()
        response = callable_obj(request, slug=client_instance.slug)
        assertContains(response, client_instance.abbreviation)

    def test_client_create_form_valid(self, client, user):
        client.force_login(user)

        form_data = {
            "name": "Happy Client",
            "abbreviation": "HPC",
            "info": "This client loves puppies",
        }
        url = reverse("projects:client_add")
        response = client.post(url, form_data)

        queried_client = Client.objects.get(abbreviation=form_data["abbreviation"])

        assert queried_client.name == form_data["name"]
        assert queried_client.abbreviation == form_data["abbreviation"]
        assert queried_client.info == form_data["info"]

    def test_client_update_view_has_correct_title(self, client, user, client_instance):
        client.force_login(user)

        url = reverse("projects:client_update", kwargs={"slug": client_instance.slug})
        response = client.get(url)
        assertContains(response, "Update Client")

    def test_client_update(self, client, user, client_instance):
        test_name = "Test_123"
        form_data = {
            "name": test_name,
            "abbreviation": client_instance.abbreviation,
            "info": client_instance.info,
        }

        url = reverse("projects:client_update", kwargs={"slug": client_instance.slug})
        client.force_login(user)
        response = client.post(url, form_data)

        client_instance.refresh_from_db()
        assert client_instance.name == test_name


class TestProjectViews:
    def test_project_list_view(self, user, rf):
        request = rf.get(reverse("projects:project_list"))
        request.user = user
        response = ProjectListView.as_view()(request)
        assertContains(response, "Project List")

    def test_project_list_view_contains_2_members(self, user, rf):

        project1 = ProjectFactory()
        project2 = ProjectFactory()
        request = rf.get(reverse("projects:project_list"))
        request.user = user
        response = ProjectListView.as_view()(request)
        assertContains(response, project1.abbreviation)
        assertContains(response, project2.abbreviation)

    def test_project_detail_view(self, user, rf, project):
        url = reverse("projects:project_detail", kwargs={"slug": project.slug})
        request = rf.get(url)
        request.user = user
        callable_obj = ProjectDetailView.as_view()
        response = callable_obj(request, slug=project.slug)
        assertContains(response, project.abbreviation)

    def test_project_create_form_valid(self, client, user):
        form_data = {
            "name": "Happy Project",
            "abbreviation": "HP",
            "info": "A project about puppies",
            "client": "",
        }

        url = reverse("projects:project_add")
        client.force_login(user)
        response = client.post(url, form_data)

        queried_project = Project.objects.get(abbreviation=form_data["abbreviation"])
        assert queried_project.name == form_data["name"]
        assert queried_project.abbreviation == form_data["abbreviation"]
        assert queried_project.info == form_data["info"]

    def test_project_update_view_has_correct_title(self, client, user, project):
        client.force_login(user)

        url = reverse("projects:projects_update", kwargs={"slug": project.slug})

        response = client.get(url)
        assertContains(response, "Update Project")

    def test_project_update(self, client, user, project):
        test_name = "Test_123"
        form_data = {
            "name": test_name,
            "abbreviation": project.abbreviation,
            "info": project.info,
        }

        url = reverse("projects:projects_update", kwargs={"slug": project.slug})
        client.force_login(user)
        response = client.post(url, form_data)

        project.refresh_from_db()
        assert project.name == test_name
