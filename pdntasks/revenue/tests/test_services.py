import pytest
import datetime

from pdntasks.revenue.models import Invoice
from pdntasks.revenue.services import (
    get_quarter_from_date,
    get_start_date_for_quarter,
    get_end_date_for_quarter,
    get_previous_quarter,
    get_total_revenue_vat_from_invoices,
)
from pdntasks.revenue.tests.factories import InvoiceFactory

pytestmark = pytest.mark.django_db


class TestQuarterOperations:
    def test_get_quarter_from_date(self):

        q1_date = datetime.date(2021, 3, 31)
        assert get_quarter_from_date(q1_date) == 1

        q2_date = datetime.date(2021, 4, 1)
        assert get_quarter_from_date(q2_date) == 2

        q3_date = datetime.date(2021, 7, 1)
        assert get_quarter_from_date(q3_date) == 3

        q4_date = datetime.date(2021, 10, 1)
        assert get_quarter_from_date(q4_date) == 4

    def test_get_start_date_for_quarter_valid(self):
        q1_start_date = datetime.date(2021, 1, 1)
        assert get_start_date_for_quarter(1, 2021) == q1_start_date

        q2_start_date = datetime.date(2021, 4, 1)
        assert get_start_date_for_quarter(2, 2021) == q2_start_date

        q3_start_date = datetime.date(2021, 7, 1)
        assert get_start_date_for_quarter(3, 2021) == q3_start_date

        q4_start_date = datetime.date(2021, 10, 1)
        assert get_start_date_for_quarter(4, 2021) == q4_start_date

    def test_get_start_date_for_quarter_invalid(self):
        with pytest.raises(ValueError):
            get_start_date_for_quarter(5, 2021)

    def test_get_end_date_for_quarter_valid(self):
        q1_end_date = datetime.date(2021, 3, 31)
        assert get_end_date_for_quarter(1, 2021) == q1_end_date

        q2_end_date = datetime.date(2021, 6, 30)
        assert get_end_date_for_quarter(2, 2021) == q2_end_date

        q3_end_date = datetime.date(2021, 9, 30)
        assert get_end_date_for_quarter(3, 2021) == q3_end_date

        q4_end_date = datetime.date(2021, 12, 31)
        assert get_end_date_for_quarter(4, 2021) == q4_end_date

    def test_get_end_date_for_quarter_invalid(self):
        with pytest.raises(ValueError):
            get_end_date_for_quarter(5, 2021)

    def test_get_previous_quarter_valid(self):
        previous_quarter = 4
        previous_year = 2020
        previous_quarter_tuple = (previous_quarter, previous_year)
        assert get_previous_quarter(1, 2021) == previous_quarter_tuple

        year = 2021

        for quarter in range(2, 5):
            previous_quarter = quarter - 1
            previous_quarter_tuple = (previous_quarter, year)
            assert get_previous_quarter(quarter, year) == previous_quarter_tuple

    def test_get_previous_quarter_invalid(self):
        with pytest.raises(ValueError):
            get_previous_quarter(5, 2021)


class TestInvoiceOperations:
    def test_get_total_revenue_vat_from_invoices(self):
        for i in range(5):

            InvoiceFactory(paid=True, invoice_amount=10.00, vat_amount=1.00)

        invoices = Invoice.objects.all()

        total_dict = get_total_revenue_vat_from_invoices(invoices)

        assert total_dict["revenue"] == 50.00
        assert total_dict["vat"] == 5.00
