from datetime import timedelta, date

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from model_utils import Choices, FieldTracker
from model_utils.models import StatusModel, TimeStampedModel


class Task(StatusModel):
    STATUS = Choices("open", "waiting", "inactive", "active", "paused", "complete")
    PERIOD = Choices("daily", "weekly", "bi-weekly", "monthly", "quarterly", "yearly")

    name = models.CharField("Task Name", max_length=255)
    info = MarkdownxField("Information (Markdown)")
    assigned_to = models.ForeignKey(
        "users.User", models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="project", sep="-", unique=True)
    date_due = models.DateField("Date Due", blank=True, null=True)
    repeats = models.CharField(
        "Repeats", choices=PERIOD, blank=True, null=True, max_length=32
    )

    status_tracker = FieldTracker(fields=["status"])

    def create_repeat_task(self, period):
        period_dict = {
            "daily": timedelta(1),
            "weekly": timedelta(weeks=1),
            "bi-weekly": timedelta(weeks=2),
            "monthly": timedelta(28),
            "quarterly": timedelta(28 * 3),
            "yearly": timedelta(365),
        }
        repeat_task = Task(
            status="open",
            name=self.name,
            info=self.info,
            assigned_to=self.assigned_to,
            project=self.project,
            repeats=self.repeats,
        )
        date_due = date.today() + period_dict[period]
        repeat_task.date_due = date_due
        repeat_task.save()
        return repeat_task.id

    def save(self, *args, **kwargs):
        if (
            (self.status == "complete")
            and (self.status_tracker.has_changed("status"))
            and self.repeats
        ):
            self.create_repeat_task(self.repeats)
        super(Task, self).save(*args, **kwargs)

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
