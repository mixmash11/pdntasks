from django.db import models
from slugify import slugify


class Client(models.Model):
    name = models.CharField("Client Name", max_length=255, unique=True)
    abbreviation = models.CharField("Abbreviation", max_length=3, unique=True)
    slug = models.SlugField(unique=True)
    info = models.TextField("Information")

    def save(self, *args, **kwargs):
        self.abbreviation = self.abbreviation.upper()
        self.slug = slugify(self.abbreviation)
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.abbreviation}"


class Project(models.Model):
    name = models.CharField("Project Name", max_length=255, unique=True)
    abbreviation = models.CharField("Abbreviation", max_length=3, unique=True)
    slug = models.SlugField(unique=True)
    info = models.TextField("Information")
    client = models.ForeignKey(Client, models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.abbreviation = self.abbreviation.upper()
        self.slug = slugify(self.abbreviation)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.abbreviation}"
