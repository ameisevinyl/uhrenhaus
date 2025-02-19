# Generated by Django 5.1.3 on 2025-02-16 11:13

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Consumption Type')),
                ('unit', models.CharField(max_length=10, verbose_name='Unit (e.g., kWh, m³)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
        ),
        migrations.CreateModel(
            name='ConversionFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.FloatField(verbose_name='Conversion Factor')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('from_consumption_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversion_from', to='meters.consumptiontype', verbose_name='From Consumption Type')),
                ('to_consumption_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversion_to', to='meters.consumptiontype', verbose_name='To Consumption Type')),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True, verbose_name='Display Name')),
                ('serial_number', models.CharField(max_length=100, unique=True, verbose_name='Serial Number')),
                ('location_description', models.TextField(blank=True, null=True, verbose_name='Location Description')),
                ('install_date', models.DateField(default=datetime.date(2013, 1, 1), verbose_name='Installation Date')),
                ('deinstall_date', models.DateField(blank=True, null=True, verbose_name='Deinstallation Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('consumption_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='meters.consumptiontype', verbose_name='Consumption Type')),
                ('parent_meter', models.ForeignKey(blank=True, help_text='The main meter this meter is a sub-meter of, if applicable.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_meters', to='meters.meter', verbose_name='Parent Meter')),
            ],
        ),
        migrations.CreateModel(
            name='MeterReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_date', models.DateField(help_text='The actual date the meter was read.', verbose_name='Reading Date')),
                ('value', models.FloatField(verbose_name='Meter Reading Value')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='meter_readings/', verbose_name='Reading Photo')),
                ('is_estimated', models.BooleanField(default=False, help_text='Mark as estimated if the reading was not actually taken.', verbose_name='Estimated Reading')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='meters.meter', verbose_name='Meter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Read By')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Unit Name')),
                ('location', models.CharField(max_length=200, verbose_name='Location (e.g., Floor 3, Building A)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('size', models.FloatField(verbose_name='Size in square meters')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('parent_unit', models.ForeignKey(blank=True, help_text='The main unit this unit belongs to, if applicable.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_units', to='meters.unit', verbose_name='Parent Unit')),
            ],
        ),
        migrations.AddField(
            model_name='meter',
            name='unit',
            field=models.ForeignKey(help_text='The unit or room where this meter is installed.', on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='meters.unit', verbose_name='Connected Unit'),
        ),
    ]
