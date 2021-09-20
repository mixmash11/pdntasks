from crispy_forms.helper import FormHelper
from django.forms import ModelForm, DateInput

from pdntasks.revenue.models import Invoice


class InvoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Invoice
        fields = [
            "invoice_id",
            "customer",
            "invoice_date",
            "invoice_amount",
            "vat_amount",
            "paid",
            "paid_date",
            "invoice_file",
        ]
        widgets = {
            "invoice_date": DateInput(attrs={"type": "date"}),
            "paid_date": DateInput(attrs={"type": "date"}),
        }
