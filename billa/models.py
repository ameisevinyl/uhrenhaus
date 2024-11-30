from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Tenant(AbstractUser):
    """Represents a tenant (Mieter) who rents a unit."""
    name = models.CharField(max_length=150, verbose_name="Full Name")
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nickname")
    billing_address = models.TextField(verbose_name="Billing Address")
    email = models.EmailField(unique=True, verbose_name="Email Address")

    def __str__(self):
        display_name = self.nickname if self.nickname else self.name
        return f"{display_name} ({self.email})"


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


class RentalContract(models.Model):
    """Links a tenant to a unit with a rental contract."""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="rental_contracts", verbose_name="Tenant")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="rental_contracts", verbose_name="Unit")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")  # Optional end date
    contract_file = models.FileField(upload_to="rental_contracts/", verbose_name="Rental Contract File")

    def __str__(self):
        return (
            f"Contract for {self.tenant.username} - {self.unit.name} "
            f"({self.start_date} to {self.end_date or 'Ongoing'})"
        )


class Rent(models.Model):
    """Represents the rent details for a specific period within a rental contract."""
    rental_contract = models.ForeignKey(
        RentalContract, on_delete=models.CASCADE, related_name="rents", verbose_name="Rental Contract"
    )
    net_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net Rent (excl. VAT)")
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="VAT Rate (%)")
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="VAT Amount", editable=False)
    gross_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Gross Rent (incl. VAT)", editable=False)
    monthly_advance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monthly Advance (incl. VAT)")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")  # Optional end date

    def save(self, *args, **kwargs):
        """Calculate VAT amount and gross rent."""
        self.vat_amount = self.net_rent * self.vat_rate / 100
        self.gross_rent = self.net_rent + self.vat_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Rent {self.start_date} to {self.end_date or 'Ongoing'}: "
            f"Net: {self.net_rent:.2f} EUR, VAT: {self.vat_amount:.2f} EUR, "
            f"Gross: {self.gross_rent:.2f} EUR, Monthly Advance: {self.monthly_advance:.2f} EUR"
        )
