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
    get_total_revenue_vat_from_invoices,
    get_projected_revenue_tax,
)


class RevenueDashboard(LoginRequiredMixin, TemplateView):

    template_name = "revenue/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        today = datetime.date.today()
        first = today.replace(day=1)
        previous_month = first - datetime.timedelta(days=1)
        context["today"] = today.strftime("%x")

        # QuerySets for invoices (year, current quarter, previous quarter)
        current_year_invoices = Invoice.get_invoices_from_year(user, today.year)
        current_month_invoices = Invoice.get_invoices_from_month(
            user, today.month, today.year
        )
        previous_month_invoices = Invoice.get_invoices_from_month(
            user, previous_month.month, today.year
        )

        # Total dicts
        ytd_totals = get_total_revenue_vat_from_invoices(current_year_invoices)
        previous_month_totals = get_total_revenue_vat_from_invoices(
            previous_month_invoices
        )
        current_month_totals = get_total_revenue_vat_from_invoices(
            current_month_invoices
        )
        projected_values = get_projected_revenue_tax(ytd_totals["revenue"], today.month)

        context["ytd_revenue"] = ytd_totals["revenue"]
        context["ytd_vat"] = ytd_totals["vat"]
        context["ytd_tax"] = ytd_totals["tax"]
        context["current_month_revenue"] = current_month_totals["revenue"]
        context["current_month_vat"] = current_month_totals["vat"]
        context["previous_month_revenue"] = previous_month_totals["revenue"]
        context["previous_month_vat"] = previous_month_totals["vat"]
        context["proj_revenue"] = projected_values["revenue"]
        context["proj_taxable_revenue"] = projected_values["taxable_revenue"]
        context["proj_tax"] = projected_values["tax"]
        context["proj_payment"] = projected_values["payment"]

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


class InvoiceDetailView(LoginRequiredMixin, DetailView):
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
        month = kwargs["month"]

        filename = f"Invoices_{year}-{month}.zip"

        invoices = Invoice.objects.filter(
            user=user, paid_date__year=year, paid_date__month=month
        )

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        with zipfile.ZipFile(response, "w") as zip_file:

            for invoice in invoices:
                file_stream = invoice.invoice_file.file.open()
                file_name = path.basename(invoice.invoice_file.name)
                zip_file.writestr(file_name, file_stream.read())

        return response
