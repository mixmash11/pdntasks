import datetime

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

from .factories import InvoiceFactory
from ..models import Invoice
from ..views import InvoiceListView, InvoiceDetailView
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def invoice():
    return InvoiceFactory()


@pytest.fixture
def user():
    return UserFactory()


class TestInvoiceListView:
    def test_invoice_list_view(self, rf):
        request = rf.get(reverse("revenue:invoice_list"))
        response = InvoiceListView.as_view()(request)
        assertContains(response, "Invoice List")

    def test_invoice_list_contains_2_invoices(self, rf):
        invoice_1 = InvoiceFactory()
        invoice_2 = InvoiceFactory()
        request = rf.get(reverse("revenue:invoice_list"))
        response = InvoiceListView.as_view()(request)
        assertContains(response, invoice_1.invoice_id)
        assertContains(response, invoice_2.invoice_id)


class TestInvoiceDetailView:
    def test_invoice_detail_view(self, rf, invoice):
        url = reverse("revenue:invoice_detail", kwargs={"pk": invoice.pk})
        request = rf.get(url)
        callable_obj = InvoiceDetailView.as_view()
        response = callable_obj(request, pk=invoice.pk)
        assertContains(response, invoice.invoice_id)


class TestInvoiceFormViews:
    def test_invoice_create_view(self, client):
        url = reverse("revenue:invoice_add")
        response = client.get(url)
        assert response.status_code == 200

    def test_invoice_create_view_has_correct_title(self, client):
        url = reverse("revenue:invoice_add")
        response = client.get(url)
        assertContains(response, "Add Invoice")

    def test_invoice_create_view_form_valid(self, client, user):
        invoice_id = "TEST123"

        form_data = {
            "invoice_id": invoice_id,
            "user": user.pk,
            "customer": "A CUSTOMER",
            "invoice_date": datetime.date.today(),
            "invoice_amount": 100.11,
            "vat_amount": 19.99,
            "paid": False,
            "paid_date": "",
            "invoice_file": "",
        }
        url = reverse("revenue:invoice_add")
        response = client.post(url, form_data)

        invoice = Invoice.objects.get()

        assert invoice.invoice_id == invoice_id

    def test_invoice_update_view_has_correct_title(self, client, invoice):
        url = reverse("revenue:invoice_update", kwargs={"pk": invoice.pk})
        response = client.get(url)
        assertContains(response, "Update Invoice")

    def test_invoice_update(self, client, invoice):

        new_invoice_amount = 1234.55
        form_data = {
            "customer": invoice.customer,
            "invoice_date": invoice.invoice_date,
            "invoice_amount": new_invoice_amount,
            "vat_amount": invoice.vat_amount,
            "paid": invoice.paid,
            "paid_date": invoice.paid_date,
            "invoice_file": invoice.invoice_file,
        }
        url = reverse("revenue:invoice_update", kwargs={"pk": invoice.pk})
        response = client.post(url, form_data)
        invoice.refresh_from_db()
        assert invoice.invoice_amount == new_invoice_amount
