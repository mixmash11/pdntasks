from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path(route="", view=views.TaskListView.as_view(), name="task_list"),
    path(
        route="unassigned/",
        view=views.UnassignedTaskListView.as_view(),
        name="unassigned_task_list",
    ),
    path(
        route="waiting/",
        view=views.WaitingTaskListView.as_view(),
        name="waiting_task_list",
    ),
    path(
        route="inactive/",
        view=views.InactiveTaskListView.as_view(),
        name="inactive_task_list",
    ),
    path(
        route="completed/",
        view=views.CompletedTaskListView.as_view(),
        name="complete_task_list",
    ),
    path(route="add/", view=views.TaskCreateView.as_view(), name="task_add"),
    path(
        route="<slug:slug>/update/",
        view=views.TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(route="<slug:slug>/", view=views.TaskDetailView.as_view(), name="task_detail"),
    path(
        route="<slug:task_slug>/add_note/",
        view=views.NoteCreateView.as_view(),
        name="note_add",
    ),
    path(
        route="notes/<slug:slug>/update/",
        view=views.NoteUpdateView.as_view(),
        name="note_update",
    ),
]
