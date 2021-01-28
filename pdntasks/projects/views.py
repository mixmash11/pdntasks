from django.views.generic import ListView, DetailView

from .models import Client, Project


class ClientListView(ListView):
    model = Client
    ordering = ["name"]


class ClientDetailView(DetailView):
    model = Client


class ProjectListView(ListView):
    model = Project
    ordering = ["name"]


class ProjectDetailView(DetailView):
    model = Project
