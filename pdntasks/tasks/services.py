import random


def create_email_text(action, user, url, slug):
    """
    Generates text for an email notifing a user about a task status change

    :param basestring action: a string describing the action taken on the task
    :param basestring user: the user who performed the action
    :param basestring url: task absolute url
    :param basestring slug: slug from the task
    :return: basestring
    """

    action_statement = f""


def get_random_queryset_samples(queryset, max_k=5):
    """
    Gets a random unique sample from a queryset, returning either a list of queryset entries or an empty list.
    If there are equal or more values than "max" in the sample set, returns a list of "max" length, otherwise returns a
    list that is equal to the length of the queryset.

    :param django.db.models.query.QuerySet queryset: queryset to sample from
    :param int max_k: the maximum number of elements to return
    :return: list
    """
    len_queryset = len(queryset)
    if len_queryset > 0 and len_queryset >= max_k:
        return random.sample(list(queryset), k=max_k)
    elif len_queryset > 0:
        return list(queryset)
    else:
        return []
