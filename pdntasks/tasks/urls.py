from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path(route="", view=views.TaskListView.as_view(), name="task_list"),
    path(route="<slug:slug>/", view=views.TaskDetailView.as_view(), name="task_detail"),
]
