from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Task, Note, Goal

admin.site.register(Task, MarkdownxModelAdmin)
admin.site.register(Note, MarkdownxModelAdmin)
admin.site.register(Goal, MarkdownxModelAdmin)
