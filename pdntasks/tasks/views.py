from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    ordering = ["-status_changed"]


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["name", "status", "assigned_to", "project", "parent_task", "info"]


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["name", "status", "assigned_to", "project", "parent_task", "info"]
    action = "Update"
