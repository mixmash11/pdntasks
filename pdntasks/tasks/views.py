from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Task, Note


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    ordering = ["-status_changed"]


class UserTaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            assigned_to=self.request.user,
            status__in=["open", "waiting", "active", "paused"],
        ).order_by("-status_changed")

    filter = "My"


class UnassignedTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(assigned_to__isnull=True).order_by("-status_changed")
    template_name = "tasks/task_list.html"
    filter = "Unassigned"


class WaitingTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="waiting").order_by("-status_changed")
    template_name = "tasks/task_list.html"
    filter = "Waiting on Response"


class InactiveTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="inactive").order_by("-status_changed")
    template_name = "tasks/task_list.html"
    filter = "Inactive"


class CompletedTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="complete").order_by("-status_changed")
    template_name = "tasks/task_list.html"
    filter = "Completed"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["notes"] = Note.objects.filter(task=context["task"]).order_by("created")
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["name", "status", "assigned_to", "project", "info"]


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["name", "status", "assigned_to", "project", "info"]
    action = "Update"


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["text"]

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, slug=kwargs["task_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = self.task
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["text"]
    action = "Update"
