from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

from pdntasks.users.models import User


class Invoice(TimeStampedModel):
    invoice_id = models.CharField("Invoice Number", max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField("Customer", max_length=32)
    invoice_date = models.DateField("Invoice Date")
    invoice_amount = models.FloatField("Invoice Amount")
    vat_amount = models.FloatField("MwSt Amount")
    paid = models.BooleanField("Paid", default=False)
    paid_date = models.DateField("Paid Date", null=True, blank=True)
    invoice_file = models.FileField(
        "Invoice File", blank=True, null=True, upload_to="invoices/%Y%m%d_%h%M/"
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"], name="user_invoice_idx"),
            models.Index(fields=["user", "invoice_date"], name="user_date_invoice_idx"),
        ]

    def __str__(self):
        return self.invoice_id

    def get_absolute_url(self):
        return reverse("revenue:invoice_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_invoices_from_quarter(user, quarter, year):

        invoices = Invoice.objects.filter(
            user=user, paid_date__year=year, paid_date__quarter=quarter
        )

        return invoices

    @staticmethod
    def get_invoices_from_year(user, year):

        invoices = Invoice.objects.filter(user=user, paid_date__year=year)

        return invoices
