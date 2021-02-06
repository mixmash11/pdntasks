from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Client, Project

admin.site.register(Client, MarkdownxModelAdmin)
admin.site.register(Project, MarkdownxModelAdmin)
