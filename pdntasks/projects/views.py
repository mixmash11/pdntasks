from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Client, Project


class ClientListView(ListView):
    model = Client
    ordering = ["name"]


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ["name", "abbreviation", "info"]


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["name", "abbreviation", "info"]
    action = "Update"


class ProjectListView(ListView):
    model = Project
    ordering = ["name"]


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreateView(CreateView):
    model = Project
    fields = ["name", "abbreviation", "info", "client"]


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["name", "abbreviation", "info"]
    action = "Update"
