from django.urls import path
from . import views

app_name = "revenue"
urlpatterns = [
    path(route="", view=views.RevenueDashboard.as_view(), name="dashboard"),
    path(route="invoices/", view=views.InvoiceListView.as_view(), name="invoice_list"),
    path(
        route="invoices/export/<int:year>/<int:month>/",
        view=views.InvoiceZIPView.as_view(),
        name="invoice_export",
    ),
    path(
        route="invoices/add/",
        view=views.InvoiceCreateView.as_view(),
        name="invoice_add",
    ),
    path(
        route="invoices/<int:pk>/update/",
        view=views.InvoiceUpdateView.as_view(),
        name="invoice_update",
    ),
    path(
        route="invoices/<int:pk>/",
        view=views.InvoiceDetailView.as_view(),
        name="invoice_detail",
    ),
]
