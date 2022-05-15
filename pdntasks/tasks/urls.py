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
    path(route="goals/", view=views.UserGoalListView.as_view(), name="goal_list"),
    path(route="goals/add/", view=views.GoalCreateView.as_view(), name="goal_add"),
    path(
        route="goals/<slug:slug>/update/",
        view=views.GoalUpdateView.as_view(),
        name="goal_update",
    ),
    path(
        route="goals/<slug:slug>/delete/",
        view=views.GoalDeleteView.as_view(),
        name="goal_delete",
    ),
    path(
        route="goals/<slug:slug>/",
        view=views.GoalDetailView.as_view(),
        name="goal_detail",
    ),
    path(route="add/", view=views.TaskCreateView.as_view(), name="task_add"),
    path(
        route="<slug:slug>/update/",
        view=views.TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        route="<slug:slug>/delete/",
        view=views.TaskDeleteView.as_view(),
        name="task_delete",
    ),
    path(route="<slug:slug>/", view=views.TaskDetailView.as_view(), name="task_detail"),
    path(
        route="<slug:task_slug>/add_note/",
        view=views.NoteCreateView.as_view(),
        name="note_add",
    ),
    path(
        route="<slug:task_slug>/notes/",
        view=views.NoteListView.as_view(),
        name="note_list",
    ),
    path(
        route="notes/<slug:slug>/update/",
        view=views.NoteUpdateView.as_view(),
        name="note_update",
    ),
]
