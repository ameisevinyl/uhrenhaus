from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(AbstractUser):
    """
    Extends Django's User model to include customer and supplier details.
    A contact can have multiple addresses.
    """
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Company Name"))
    customer_number = models.CharField(max_length=50, unique=True, verbose_name=_("Customer Number"))
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Tax Number"))
    uid_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("UID Number (VAT)"))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone Number"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))  # ✅ Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))  # ✅ Auto-update timestamp

    class Meta:
        ordering = ["-created_at"]  # ✅ Show newest contacts first

    def __str__(self):
        """Show company name if available, otherwise username."""
        return f"{self.company_name or self.username} ({self.email})"


class Address(models.Model):
    """
    A structured address following ISO standards.
    Each contact can have multiple addresses.
    """
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="addresses")
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address Type"))

    country = models.CharField(max_length=2, verbose_name=_("Country"), help_text="ISO 3166-1 alpha-2 code (e.g., DE, US)")
    address_line_1 = models.CharField(max_length=255, verbose_name=_("Address Line 1"))
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address Line 2"))
    address_line_3 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address Line 3"))
    
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal Code"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("State/Province/Region"))
    
    is_residential = models.BooleanField(default=False, verbose_name=_("Is this a residential address?"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))  # ✅ Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))  # ✅ Auto-update timestamp

    class Meta:
        ordering = ["-created_at"]  # ✅ Show newest addresses first

    def __str__(self):
        """Generate a structured address string."""
        parts = [self.address_line_1]
        if self.address_line_2:
            parts.append(self.address_line_2)
        if self.address_line_3:
            parts.append(self.address_line_3)
        parts.append(f"{self.postal_code} {self.city}, {self.country}")
        if self.is_residential:
            parts.append("(Residential)")
        return " - ".join(parts)

class BankAccount(models.Model):
    """
    Stores bank account details for a contact.
    A contact can have multiple bank accounts.
    """
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="bank_accounts", verbose_name=_("Contact")
    )
    account_holder = models.CharField(max_length=255, verbose_name=_("Account Holder Name"))
    iban = models.CharField(max_length=34, unique=True, verbose_name=_("IBAN"))
    bic = models.CharField(max_length=11, blank=True, null=True, verbose_name=_("BIC/SWIFT"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")

    def __str__(self):
        return f"{self.account_holder} - {self.iban}"
