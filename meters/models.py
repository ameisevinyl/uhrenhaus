from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings  # Import user model


class Unit(models.Model):
    """Represents a location in the building, such as rooms or units."""
    name = models.CharField(max_length=100, verbose_name=_("Unit Name"))
    location = models.CharField(max_length=200, verbose_name=_("Location (e.g., Floor 3, Building A)"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    size = models.FloatField(verbose_name=_("Size in square meters"))
    parent_unit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sub_units",
        verbose_name=_("Parent Unit"),
        help_text=_("The main unit this unit belongs to, if applicable.")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"{self.name} ({self.location})"


class ConsumptionType(models.Model):
    """Defines the type of utility being consumed (e.g., electricity, gas, water)."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Consumption Type"))
    unit = models.CharField(max_length=10, verbose_name=_("Unit (e.g., kWh, m³)"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Meter(models.Model):
    """Represents a physical utility meter connected to a specific consumption type and building unit."""
    label = models.CharField(max_length=100, unique=True, verbose_name=_("Display Name"))
    serial_number = models.CharField(max_length=100, unique=True, verbose_name=_("Serial Number"))
    consumption_type = models.ForeignKey(
        ConsumptionType, on_delete=models.CASCADE, related_name="meters", verbose_name=_("Consumption Type")
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="meters", verbose_name=_("Connected Unit"),
        help_text=_("The unit or room where this meter is installed.")
    )
    location_description = models.TextField(blank=True, null=True, verbose_name=_("Location Description"))

    parent_meter = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sub_meters",
        verbose_name=_("Parent Meter"),
        help_text=_("The main meter this meter is a sub-meter of, if applicable.")
    )

    install_date = models.DateField(default=date(2013, 1, 1), verbose_name=_("Installation Date"))
    deinstall_date = models.DateField(blank=True, null=True, verbose_name=_("Deinstallation Date"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"Meter {self.serial_number} ({self.consumption_type.name}) in {self.unit.name}"


class ConversionFactor(models.Model):
    """Stores the factor to convert one consumption type to another within a valid date range."""
    from_consumption_type = models.ForeignKey(
        ConsumptionType,
        on_delete=models.CASCADE,
        related_name="conversion_from",
        verbose_name=_("From Consumption Type")
    )
    to_consumption_type = models.ForeignKey(
        ConsumptionType,
        on_delete=models.CASCADE,
        related_name="conversion_to",
        verbose_name=_("To Consumption Type")
    )
    factor = models.FloatField(verbose_name=_("Conversion Factor"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def clean(self):
        """Ensure valid date range and prevent self-conversion."""
        if self.from_consumption_type == self.to_consumption_type:
            raise ValidationError(_("Conversion cannot be from and to the same consumption type."))
        if self.start_date >= self.end_date:
            raise ValidationError(_("Start date must be before end date."))

    def __str__(self):
        return (
            f"Convert {self.from_consumption_type.name} → {self.to_consumption_type.name} "
            f"at {self.factor} (Valid: {self.start_date} to {self.end_date})"
        )


class MeterReading(models.Model):
    """
    Stores meter readings linked to meters and users.
    Allows estimated readings when real data is unavailable.
    """
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name="readings", verbose_name=_("Meter"))
    reading_date = models.DateField(verbose_name=_("Reading Date"), help_text=_("The actual date the meter was read."))
    value = models.FloatField(verbose_name=_("Meter Reading Value"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Read By"))
    photo = models.ImageField(upload_to="meter_readings/", blank=True, null=True, verbose_name=_("Reading Photo"))

    is_estimated = models.BooleanField(default=False, verbose_name=_("Estimated Reading"), help_text=_("Mark as estimated if the reading was not actually taken."))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        estimate_label = " (Estimated)" if self.is_estimated else ""
        return f"Reading {self.value} for {self.meter.label} on {self.reading_date}{estimate_label}"
