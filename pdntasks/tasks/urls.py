from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path(route="", view=views.TaskListView.as_view(), name="task_list"),
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
