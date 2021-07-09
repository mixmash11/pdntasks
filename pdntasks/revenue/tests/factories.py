# revenue/tests/factories.py
import datetime

import factory
import factory.fuzzy

from ..models import Invoice
from ...users.tests.factories import UserFactory


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    invoice_id = factory.Faker("bothify", text="####-#####???")
    user = factory.SubFactory(UserFactory)
    customer = factory.Faker("company")
    invoice_date = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today()
    )
    invoice_amount = factory.fuzzy.FuzzyFloat(low=50.00, high=8000.00)
    vat_amount = factory.fuzzy.FuzzyFloat(low=9.50, high=3500.55)
    paid = factory.Faker("pybool")
    paid_date = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today()
    )
    invoice_file = factory.django.FileField()
