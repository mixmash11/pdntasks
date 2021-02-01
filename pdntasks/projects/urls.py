from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path(route="clients/", view=views.ClientListView.as_view(), name="client_list"),
    path(
        route="clients/add_client/",
        view=views.ClientCreateView.as_view(),
        name="client_add",
    ),
    path(
        route="clients/<slug:slug>/update/",
        view=views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        route="clients/<slug:slug>/",
        view=views.ClientDetailView.as_view(),
        name="client_detail",
    ),
    path(route="projects/", view=views.ProjectListView.as_view(), name="project_list"),
    path(
        route="projects/add_project/",
        view=views.ProjectCreateView.as_view(),
        name="project_add",
    ),
    path(
        route="projects/<slug:slug>/update/",
        view=views.ProjectUpdateView.as_view(),
        name="projects_update",
    ),
    path(
        route="projects/<slug:slug>/",
        view=views.ProjectDetailView.as_view(),
        name="project_detail",
    ),
]
