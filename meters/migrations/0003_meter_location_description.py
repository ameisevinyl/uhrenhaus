# Generated by Django 5.1.3 on 2024-12-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0002_conversionfactor'),
    ]

    operations = [
        migrations.AddField(
            model_name='meter',
            name='location_description',
            field=models.TextField(blank=True, null=True, verbose_name='Where to find this meter?'),
        ),
    ]
