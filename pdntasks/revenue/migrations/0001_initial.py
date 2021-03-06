# Generated by Django 3.0.10 on 2021-07-05 12:27

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('customer', models.CharField(max_length=32, verbose_name='Customer')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('invoice_amount', models.FloatField(verbose_name='Invoice Amount')),
                ('vat_amount', models.FloatField(verbose_name='MwSt Amount')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('paid_date', models.DateField(verbose_name='Paid Date')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
