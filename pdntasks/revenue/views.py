import datetime
import zipfile
from os import path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)

from .forms import InvoiceForm
from .models import Invoice
from .services import (
    get_quarter_from_date,
    get_previous_quarter,
    get_total_revenue_vat_from_invoices,
)


class RevenueDashboard(TemplateView):

    template_name = "revenue/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        today = datetime.date.today()
        context["today"] = today.strftime("%x")
        current_quarter_number = get_quarter_from_date(today)
        previous_quarter_number, previous_year_number = get_previous_quarter(
            current_quarter_number, today.year
        )

        # QuerySets for invoices (year, current quarter, previous quarter)
        current_year_invoices = Invoice.get_invoices_from_year(user, today.year)
        current_quarter_invoices = Invoice.get_invoices_from_quarter(
            user, current_quarter_number, today.year
        )
        previous_quarter_invoices = Invoice.get_invoices_from_quarter(
            user, previous_quarter_number, previous_year_number
        )

        # Total dicts
        ytd_totals = get_total_revenue_vat_from_invoices(current_year_invoices)
        qtr_totals = get_total_revenue_vat_from_invoices(current_quarter_invoices)
        p_qtr_totals = get_total_revenue_vat_from_invoices(previous_quarter_invoices)

        context["ytd_revenue"] = ytd_totals["revenue"]
        context["ytd_costs"] = ytd_totals["vat"]
        context["current_quarter_revenue"] = qtr_totals["revenue"]
        context["current_quarter_vat"] = qtr_totals["vat"]
        context["previous_quarter_revenue"] = p_qtr_totals["revenue"]
        context["previous_quarter_vat"] = p_qtr_totals["vat"]

        # Get last 10 invoice for display in table
        context["invoice_list"] = Invoice.objects.filter(user=user).order_by(
            "-invoice_date"
        )[:10]

        return context


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    ordering = ["-invoice_date"]
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Invoice.objects.filter(user=self.user)
        return super().get_queryset()


class InvoiceDetailView(DetailView):
    model = Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    action = "Update"
    form_class = InvoiceForm

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get("pk", None)
        if pk:
            invoice_user = Invoice.objects.get(pk=pk).user
            if not invoice_user == user:
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class InvoiceZIPView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        user = request.user
        year = kwargs["year"]
        quarter = kwargs["quarter"]

        filename = f"Invoices_{year}-Q{quarter}.zip"

        invoices = Invoice.objects.filter(
            user=user, paid_date__year=year, paid_date__quarter=quarter
        )

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        with zipfile.ZipFile(response, "w") as zip_file:

            for invoice in invoices:
                file_stream = invoice.invoice_file.file.open()
                file_name = path.basename(invoice.invoice_file.name)
                zip_file.writestr(file_name, file_stream.read())

        return response
