from django.db import models
from django.urls import reverse
from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from autoslug import AutoSlugField


class Task(StatusModel):
    STATUS = Choices("open", "waiting", "inactive", "active", "paused", "complete")

    name = models.CharField("Task Name", max_length=255)
    info = models.TextField("Information")
    assigned_to = models.ForeignKey(
        "users.User", models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    parent_task = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    slug = AutoSlugField(populate_from="project", sep="-", unique=True)

    def __str__(self):
        return f"{self.slug}"

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"slug": self.slug})


# class Note(TimeStampedModel):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     text = models.TextField("Note")
#     user = assigned_to = models.ForeignKey(
#         "users.User", models.SET_NULL, blank=True, null=True
#     )
