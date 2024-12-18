from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

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

    def __str__(self):
        return f"{self.name} ({self.location})"
    
class ConsumptionType(models.Model):
    """Defines the type of utility being consumed (e.g., electricity, gas, water)."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Consumption Type"))
    unit = models.CharField(max_length=10, verbose_name=_("Unit (e.g., kWh, m³)"))

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Meter(models.Model):
    """Represents a physical utility meter connected to a specific consumption type and building unit."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Short name"))
    serial_number = models.CharField(max_length=100, unique=True, verbose_name=_("Serial Number"))
    consumption_type = models.ForeignKey(
        ConsumptionType, on_delete=models.CASCADE, related_name="meters", verbose_name=_("Consumption Type")
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="meters", verbose_name=_("Connected Unit"),
        help_text=_("The unit or room where this meter is installed.")
    )

    location_description = models.TextField(blank=True, null=True, verbose_name=_("Where to find this meter?2"))

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

    def __str__(self):
        return (
            f"Convert {self.from_consumption_type.name} → {self.to_consumption_type.name} "
            f"at {self.factor} (Valid: {self.start_date} to {self.end_date})"
        )