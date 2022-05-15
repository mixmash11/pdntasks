from cbvhtmx.mixins import HxMixin
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .celery_tasks import (
    send_task_status_notification_email_to_all,
    send_task_status_notification_email_to_assigned_user,
)
from .forms import TaskForm, GoalForm
from .models import Task, Note, Goal


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    ordering = ["date_due", "-status_changed"]

    filter = "Full"
    description = "A list of all tasks."


class UserTaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            assigned_to=self.request.user,
            status__in=["open", "waiting", "active", "paused"],
        ).order_by("date_due", "-status_changed")

    filter = "My"
    description = "A list of current tasks assigned to you."


class UnassignedTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(assigned_to__isnull=True).order_by(
        "date_due", "-status_changed"
    )
    template_name = "tasks/task_list.html"
    filter = "Unassigned"
    description = "A list of not unassigned tasks."


class WaitingTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="waiting").order_by(
        "date_due", "-status_changed"
    )
    template_name = "tasks/task_list.html"
    filter = "Waiting on Response"
    description = "A list of tasks where you're waiting on a reply from someone."


class InactiveTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="inactive").order_by(
        "date_due", "-status_changed"
    )
    template_name = "tasks/task_list.html"
    filter = "Inactive"
    description = "A list of inactive tasks."


class CompletedTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(status="complete").order_by(
        "date_due", "-status_changed"
    )
    template_name = "tasks/task_list.html"
    filter = "Completed"
    description = "A list of completed tasks."


class TaskDetailView(LoginRequiredMixin, HxMixin, DetailView):
    model = Task
    hx_template = "tasks/htmx/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["notes"] = Note.objects.filter(task=context["task"]).order_by("created")
        return context


class TaskCreateView(LoginRequiredMixin, HxMixin, CreateView):
    model = Task
    form_class = TaskForm
    action = "Add"

    def form_valid(self, form):
        response = super().form_valid(form)
        task = self.object

        if task.assigned_to != self.request.user:
            site_name = get_current_site(self.request).name

            if not task.assigned_to:
                subject = f"New Unassigned Task: {task.slug}"
                message = f"Task {task.slug} was created without being assigned."
                send_task_status_notification_email_to_all.delay(
                    task.pk, subject, message, str(self.request.user), site_name
                )
                return response

            subject = f"New Task assigned: {task.slug}"
            message = f"Task {task.slug} was created and assigned to you."
            send_task_status_notification_email_to_assigned_user.delay(
                task.pk, subject, message, str(self.request.user), site_name
            )

        return response


class TaskUpdateView(LoginRequiredMixin, HxMixin, UpdateView):
    model = Task
    form_class = TaskForm
    action = "Update"

    def form_valid(self, form):
        response = super().form_valid(form)

        task = self.object

        if task.assigned_to != self.request.user:
            site_name = get_current_site(self.request).name

            if not task.assigned_to:
                self.send_unassigned_task_update(site_name, task)
                return response

            self.send_user_task_update(site_name, task)

        return response

    def send_unassigned_task_update(self, site_name, task):
        subject = f"Unassigned Task Updated: {task.slug}"
        message = f"The unassigned Task {task.slug} was updated."
        send_task_status_notification_email_to_all.delay(
            task.pk, subject, message, str(self.request.user), site_name
        )

    def send_user_task_update(self, site_name, task):
        subject = f"Task updated: {task.slug}"
        message = f"Task {task.slug} was updated."
        send_task_status_notification_email_to_assigned_user.delay(
            task.pk, subject, message, str(self.request.user), site_name
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("home")


class HxTriggerFormMixin:

    hx = False
    trigger = None

    def form_valid(self, form):
        if self.hx and self.trigger:
            super().form_valid(form)
            response = HttpResponse(status=204)
            response.headers["HX-Trigger"] = self.trigger
            return response
        else:
            return super().form_valid(form)


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    task = None

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, slug=kwargs["task_slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Note.objects.filter(task=self.task).order_by("-created")
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["task"] = self.task
        return context_data


class NoteCreateView(LoginRequiredMixin, HxMixin, HxTriggerFormMixin, CreateView):
    model = Note
    fields = ["text"]
    task = None

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, slug=kwargs["task_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = self.task
        self.trigger = f"update-notes-{ self.task.slug }"
        response = super().form_valid(form)

        task = self.task

        if task.assigned_to != self.request.user:
            site_name = get_current_site(self.request).name

            if not task.assigned_to:
                self.send_unassigned_task_note_creation(site_name, task)
                return response

            self.send_user_task_note_creation(site_name, task)

        return response

    def send_unassigned_task_note_creation(self, site_name, task):
        subject = f"New Note for Unassigned Task: {task.slug}"
        message = f"The unassigned Task {task.slug} has a new note."
        send_task_status_notification_email_to_all.delay(
            task.pk, subject, message, str(self.request.user), site_name
        )

    def send_user_task_note_creation(self, site_name, task):
        subject = f"New Note for Task: {task.slug}"
        message = f"The Task {task.slug} has a new note."
        send_task_status_notification_email_to_assigned_user.delay(
            task.pk, subject, message, str(self.request.user), site_name
        )


class NoteUpdateView(LoginRequiredMixin, HxMixin, HxTriggerFormMixin, UpdateView):
    model = Note
    fields = ["text"]
    action = "Update"
    task = None

    def form_valid(self, form):
        self.task = form.instance.task
        self.trigger = f"update-notes-{ self.task.slug }"
        response = super().form_valid(form)

        if self.task.assigned_to != self.request.user:
            site_name = get_current_site(self.request).name

            if not self.task.assigned_to:
                subject = f"Note updated for Unassigned Task: {self.task.slug}"
                message = f"The unassigned Task {self.task.slug} has an updated note."
                send_task_status_notification_email_to_all.delay(
                    self.task.pk, subject, message, str(self.request.user), site_name
                )
                return response

            subject = f"Updated Note for Task: {self.task.slug}"
            message = f"The Task {self.task.slug} has an updated note."
            send_task_status_notification_email_to_assigned_user.delay(
                self.task.pk, subject, message, str(self.request.user), site_name
            )

        return response


class UserGoalListView(LoginRequiredMixin, ListView):
    model = Goal

    def get_queryset(self):
        return Goal.objects.filter(goal_user=self.request.user)


class GoalDetailView(LoginRequiredMixin, DetailView):
    model = Goal


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm

    def form_valid(self, form):
        form.instance.goal_user = self.request.user
        response = super().form_valid(form)

        return response


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    action = "Update"


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy("tasks:goal_list")
