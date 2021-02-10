from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Client, Project
from ..tasks.models import Task


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    ordering = ["name"]


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["name", "abbreviation", "info"]


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["name", "abbreviation", "info"]
    action = "Update"


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    ordering = ["name"]


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(project=context["project"]).order_by(
            "-status_changed"
        )
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["name", "abbreviation", "info", "client", "parent_project"]


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["name", "abbreviation", "info", "client", "parent_project"]
    action = "Update"
