# Generated by Django 3.0.10 on 2021-01-31 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("projects", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="client",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="client",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="project",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
