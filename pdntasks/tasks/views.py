from django.views.generic import ListView, DetailView

from .models import Task


class TaskListView(ListView):
    model = Task
    ordering = ["-status_changed"]


class TaskDetailView(DetailView):
    model = Task
