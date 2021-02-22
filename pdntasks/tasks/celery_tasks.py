from allauth.utils import build_absolute_uri
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from pdntasks.tasks.models import Task
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
    logger.info("Preparing recipient list")
    task = Task.objects.get(pk=task_pk)
    recipient_list = [task.assigned_to.email]

    send_task_notification_email(
        changed_by, message, recipient_list, site_name, subject, task_pk
    )
    logger.info("Email successfully sent")
