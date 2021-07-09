import pytest

from .factories import InvoiceFactory

pytestmark = pytest.mark.django_db


class TestInvoice:
    def test__str__(self):

        invoice_id = "TEST123"

        invoice = InvoiceFactory(invoice_id=invoice_id)

        assert invoice.__str__() == invoice_id
        assert str(invoice) == invoice_id

    def test_get_absolute_url(self):
        invoice = InvoiceFactory()
        url = invoice.get_absolute_url()
        assert url == f"/revenue/{invoice.invoice_id}"
