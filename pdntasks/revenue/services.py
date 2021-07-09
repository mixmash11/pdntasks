import datetime


def get_quarter_from_date(date):
    """
    Determines the Quarter of a year
    :param datetime.date date: date to read
    :return: int representing quarter (1-4)
    """

    return (date.month - 1) // 3 + 1


def get_start_date_for_quarter(quarter, year):
    """
    Returns the start date for a given quarter
    :param int quarter: quarter (in range 1-4)
    :param int year: year
    :return: datetime.date
    """

    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be in range 1-4!")

    month_multiplier = quarter - 1
    day = 1
    month = (month_multiplier * 3) + 1

    return datetime.date(year, month, day)


def get_end_date_for_quarter(quarter, year):
    """
    Returns the end date for a given quarter
    :param int quarter: quarter (in range 1-4)
    :param int year: year
    :return: datetime.date
    """

    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be in range 1-4!")

    elif quarter == 4:
        return datetime.date(year, 12, 31)

    else:
        next_qtr_start_date = get_start_date_for_quarter(quarter + 1, year)
        one_day = datetime.timedelta(days=1)
        return next_qtr_start_date - one_day


def get_previous_quarter(quarter, year):
    """
    Returns the end date for a given quarter
    :param int quarter: quarter (in range 1-4)
    :param int year: year
    :return: datetime.date
    """

    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be in range 1-4!")

    if quarter == 1:
        previous_year = year - 1
        return 4, previous_year
    else:
        previous_quarter = quarter - 1
        return previous_quarter, year


def get_total_revenue_vat_from_invoices(invoices):
    """
    Gets the total revenue and vat from an Invoice QuerySet
    :param django.db.models.query.QuerySet invoices: Invoice queryset
    :return: dict with keys "revenue" and "vat"
    """
    total_revenue = 0.00
    total_vat = 0.00
    for invoice in invoices:
        if invoice.paid:
            total_revenue += invoice.invoice_amount
            total_vat += invoice.vat_amount

    total_dict = {"revenue": total_revenue, "vat": total_vat}

    return total_dict
