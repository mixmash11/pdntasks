from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Task, Note

admin.site.register(Task, MarkdownxModelAdmin)
admin.site.register(Note, MarkdownxModelAdmin)
