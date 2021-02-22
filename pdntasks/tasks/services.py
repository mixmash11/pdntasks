def create_email_text(action, user, url, slug):
    """
    Generates text for an email notifing a user about a task status change

    :param basestring action: a string describing the action taken on the task
    :param basestring user: he user who performed the action
    :param basestring url: task absolute url
    :param basestring slug: slug from the task
    :return: basestring
    """

    action_statement = f""
