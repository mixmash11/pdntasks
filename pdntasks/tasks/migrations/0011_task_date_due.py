# Generated by Django 3.0.10 on 2021-02-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("tasks", "0010_remove_task_parent_task")]

    operations = [
        migrations.AddField(
            model_name="task",
            name="date_due",
            field=models.DateField(blank=True, null=True, verbose_name="Date Due"),
        )
    ]
