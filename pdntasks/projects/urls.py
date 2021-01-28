from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path(route="clients/", view=views.ClientListView.as_view(), name="client_list"),
    path(
        route="clients/<slug:slug>",
        view=views.ClientDetailView.as_view(),
        name="client_detail",
    ),
    path(route="projects/", view=views.ProjectListView.as_view(), name="project_list"),
    path(
        route="projects/<slug:slug>",
        view=views.ProjectDetailView.as_view(),
        name="project_detail",
    ),
]
