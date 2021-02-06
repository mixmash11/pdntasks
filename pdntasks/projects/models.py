from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify

from model_utils.models import TimeStampedModel


class Client(TimeStampedModel):
    name = models.CharField("Client Name", max_length=255, unique=True)
    abbreviation = models.CharField("Abbreviation", max_length=3, unique=True)
    slug = models.SlugField(unique=True)
    info = MarkdownxField("Information (Markdown)")

    @property
    def formatted_markdown(self):
        return markdownify(self.info)

    def save(self, *args, **kwargs):
        self.abbreviation = self.abbreviation.upper()
        self.slug = slugify(self.abbreviation)
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.abbreviation}"

    def get_absolute_url(self):
        return reverse("project_management:client_detail", kwargs={"slug": self.slug})


class Project(TimeStampedModel):
    name = models.CharField("Project Name", max_length=255, unique=True)
    abbreviation = models.CharField("Abbreviation", max_length=3, unique=True)
    slug = models.SlugField(unique=True)
    info = MarkdownxField("Information (Markdown)")
    client = models.ForeignKey(Client, models.SET_NULL, blank=True, null=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.info)

    def save(self, *args, **kwargs):
        self.abbreviation = self.abbreviation.upper()
        self.slug = slugify(self.abbreviation)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.abbreviation}"

    def get_absolute_url(self):
        return reverse("project_management:project_detail", kwargs={"slug": self.slug})
