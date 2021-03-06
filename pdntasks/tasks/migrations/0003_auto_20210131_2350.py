# Generated by Django 3.0.10 on 2021-01-31 22:50

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tasks", "0002_auto_20210131_2321")]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                blank=True,
                editable=False,
                null=True,
                populate_from="project",
                unique=True,
            ),
        )
    ]
