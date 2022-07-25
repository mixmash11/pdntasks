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


def calculate_income_tax(income):

    if income < 9985:
        income_tax = 0
    elif income < 14927:
        taxable_value = income - 9984
        modifier = taxable_value / 10000
        income_tax = (1008.7 * modifier + 1400) * modifier
    elif income < 58597:
        taxable_value = income - 14926
        modifier = taxable_value / 10000
        income_tax = (206.43 * modifier + 2397) * modifier + 938.24
    elif income < 277826:
        income_tax = (income * 0.42) - 9267.53
    else:
        income_tax = (income * 0.45) - 17602.28

    return income_tax


def get_projected_revenue_tax(
    current_revenue, month, quarterly_prepayment=2700.00, projected_writeoffs=7000.00
):
    average_monthly_revenue = current_revenue / month
    projected_revenue = average_monthly_revenue * 12
    projected_taxable_revenue = projected_revenue - projected_writeoffs
    projected_tax = calculate_income_tax(projected_taxable_revenue)
    projected_payment = projected_tax - (quarterly_prepayment * 4)

    projected_dict = {
        "revenue": projected_revenue,
        "taxable_revenue": projected_taxable_revenue,
        "tax": projected_tax,
        "payment": projected_payment,
    }
    return projected_dict


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

    income_tax = calculate_income_tax(total_revenue)

    total_dict = {"revenue": total_revenue, "vat": total_vat, "tax": income_tax}

    return total_dict
