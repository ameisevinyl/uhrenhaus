# Generated by Django 5.1.3 on 2024-12-03 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Consumption Type')),
                ('unit', models.CharField(max_length=10, verbose_name='Unit (e.g., kWh, m³)')),
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
                ('parent_unit', models.ForeignKey(blank=True, help_text='The main unit this unit belongs to, if applicable.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_units', to='meters.unit', verbose_name='Parent Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True, verbose_name='Serial Number')),
                ('consumption_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='meters.consumptiontype', verbose_name='Consumption Type')),
                ('parent_meter', models.ForeignKey(blank=True, help_text='The main meter this meter is a sub-meter of, if applicable.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_meters', to='meters.meter', verbose_name='Parent Meter')),
                ('unit', models.ForeignKey(help_text='The unit or room where this meter is installed.', on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='meters.unit', verbose_name='Connected Unit')),
            ],
        ),
    ]
