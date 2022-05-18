from datetime import date, timedelta

from allauth.utils import build_absolute_uri
from celery import shared_task
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string, get_template

from pdntasks.tasks.models import Task, Goal
from pdntasks.tasks.services import get_random_queryset_samples
from pdntasks.users.models import User

import logging

logger = logging.getLogger(__name__)


def send_task_notification_email(
    changed_by, message, recipient_list, site_name, subject, task_pk
):
    logger.info("Preparing email")
    site_domain = build_absolute_uri(None, "")
    task = Task.objects.get(pk=task_pk)
    task_url = build_absolute_uri(None, task.get_absolute_url())
    subject = f"[{site_name}] {subject}"
    change_message = message
    param_dict = {
        "subject": subject,
        "site_name": site_name,
        "site_domain": site_domain,
        "user_name": changed_by,
        "task_url": task_url,
        "task_abb": task,
        "change_message": change_message,
    }

    logger.info("Rendering email")
    msg_plain = render_to_string("tasks/email/task_notification_email.txt", param_dict)

    logger.info("Sending email")
    send_mail(subject, msg_plain, None, recipient_list)
    return 0


@shared_task
def send_task_status_notification_email_to_all(
    task_pk, subject, message, changed_by, site_name
):
    """
    Send a task notification to all users
    :param int task_pk:
    :param basestring subject:
    :param basestring message:
    :param basestring changed_by:
    :param basestring site_name:
    """

    logger.info("Preparing recipient list")
    recipient_list = User.objects.values_list("email", flat=True)

    send_task_notification_email(
        changed_by, message, recipient_list, site_name, subject, task_pk
    )
    logger.info("Email successfully sent")
    return 0


@shared_task
def send_task_status_notification_email_to_assigned_user(
    task_pk, subject, message, changed_by, site_name
):
    """
    Send a task notification to the user assigned the task
    :param int task_pk:
    :param basestring subject:
    :param basestring message:
    :param basestring changed_by:
    :param basestring site_name:
    """
    logger.info("START - SEND TASK STATUS NOTIFICATION (ASSIGNED USER)")
    logger.info("Preparing recipient list")
    task = Task.objects.get(pk=task_pk)
    recipient_list = [task.assigned_to.email]

    send_task_notification_email(
        changed_by, message, recipient_list, site_name, subject, task_pk
    )
    logger.info("Email successfully sent")
    logger.info("STOP - SEND TASK STATUS NOTIFICATION (ASSIGNED USER)")
    return 0


@shared_task
def reset_overdue_task_due_date():
    logger.info("START - RESET OVERDUE TASKS")
    today = date.today()
    overdue_tasks = Task.objects.filter(
        date_due__lt=today, status__in=["open", "waiting", "active"]
    )
    for task in overdue_tasks:
        logger.info(f"START - RESET OVERDUE TASK: {task.name}")
        task.date_due = today
        task.save()
        logger.info(f"STOP - RESET OVERDUE TASK: {task.name}")
    logger.info("STOP - RESET OVERDUE TASKS")
    return 0


@shared_task
def send_daily_email(user_pk, site_name):
    logger.info("START - SEND DAILY EMAIL")

    logger.info("Preparing email")
    user = User.objects.get(pk=user_pk)

    today = date.today()
    tomorrow = today + timedelta(1)
    one_week_date = today + timedelta(6)

    user_tasks = Task.objects.filter(assigned_to=user)
    todays_tasks = user_tasks.filter(date_due=today)
    week_tasks = user_tasks.filter(date_due__range=(tomorrow, one_week_date))
    undated_tasks = get_random_queryset_samples(
        user_tasks.filter(date_due__isnull=True), max_k=5
    )
    goals = Goal.objects.filter(goal_user=user)

    if len(todays_tasks) < 1:
        logger.info("No tasks due today.")
        logger.info("STOP - SEND DAILY EMAIL")
        return 0

    email_content = {
        "user_name": str(user),
        "today": today,
        "todays_tasks": todays_tasks,
        "week_tasks": week_tasks,
        "undated_tasks": undated_tasks,
        "goals": goals,
        "site_name": site_name,
        "site_domain": build_absolute_uri(None, ""),
    }
    subject = f"Daily Intro for {today.strftime('%A, %B %d')}"

    logger.info("Rendering email")
    plain_email = render_to_string("tasks/email/daily_task_email.txt", email_content)
    html_email = render_to_string("tasks/email/daily_task_email.html", email_content)

    logger.info("Sending email")
    emails_sent = send_mail(
        subject, plain_email, None, [user.email], html_message=html_email
    )
    if emails_sent > 0:
        logger.info("Email sent sucessfully.")
    else:
        logger.info("Email not sent.")
    logger.info("STOP - SEND DAILY EMAIL")

    return 0


@shared_task
def arrange_daily_emails():
    daily_email_users = User.objects.filter(daily_email=True)

    site_name = Site.objects.get_current().domain

    for user in daily_email_users:
        send_daily_email.delay(user.pk, site_name)
