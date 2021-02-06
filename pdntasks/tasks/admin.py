from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Task

admin.site.register(Task, MarkdownxModelAdmin)
