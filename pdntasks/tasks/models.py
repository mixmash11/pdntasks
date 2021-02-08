from django.db import models
from django.urls import reverse
from markdownx.utils import markdownify
from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices
from autoslug import AutoSlugField
from markdownx.models import MarkdownxField


class Task(StatusModel):
    STATUS = Choices("open", "waiting", "inactive", "active", "paused", "complete")

    name = models.CharField("Task Name", max_length=255)
    info = MarkdownxField("Information (Markdown)")
    assigned_to = models.ForeignKey(
        "users.User", models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    parent_task = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    slug = AutoSlugField(populate_from="project", sep="-", unique=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.info)

    def __str__(self):
        return f"{self.slug}"

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"slug": self.slug})


class Note(TimeStampedModel):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = MarkdownxField("Text (Markdown)")
    user = models.ForeignKey("users.User", models.SET_NULL, blank=True, null=True)
    slug = AutoSlugField(populate_from="task", sep="-", unique=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return f"{self.slug}"

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"slug": self.task.slug})
