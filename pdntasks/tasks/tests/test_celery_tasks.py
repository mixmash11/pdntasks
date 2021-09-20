from datetime import date, timedelta

import pytest

from ..celery_tasks import reset_overdue_task_due_date
from ..models import Task
from .factories import TaskFactory

pytestmark = pytest.mark.django_db


def test_reset_overdue_task_due_date():
    today = date.today()
    delta = -2

    for i in range(5):
        entry_delta = delta + i
        date_entry = today + timedelta(entry_delta)
        TaskFactory(date_due=date_entry)

    assert Task.objects.filter(date_due__lt=today).count() == 2
    assert Task.objects.filter(date_due=today).count() == 1
    assert Task.objects.filter(date_due__gt=today).count() == 2

    reset_overdue_task_due_date()

    assert Task.objects.filter(date_due=today).count() == 3
    assert Task.objects.filter(date_due__gt=today).count() == 2
