from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, Address, BankAccount


class AddressInline(admin.TabularInline):  # Allows inline editing of addresses within a contact
    model = Address
    extra = 1  # Show one empty address form by default


@admin.register(Contact)
class ContactAdmin(UserAdmin):
    """
    Admin panel configuration for Contact.
    Extends Django's default UserAdmin for better contact management.
    """
    model = Contact
    inlines = [AddressInline]  # Allows managing addresses inside Contact view

    fieldsets = UserAdmin.fieldsets + (
        ("Contact Details", {"fields": ("company_name", "customer_number", "tax_number", "uid_number", "phone_number")}),
    )

    list_display = ("username", "email", "company_name", "customer_number", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("username", "email", "company_name", "customer_number")
    ordering = ("username",)  # Default ordering by username



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Address.
    Allows listing, searching, and filtering addresses.
    """
    list_display = ("contact", "address_line_1", "city", "postal_code", "country", "is_residential")
    search_fields = ("contact__username", "address_line_1", "city", "postal_code")
    list_filter = ("country", "is_residential")
    ordering = ("contact", "city")  # Default ordering by contact and city

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("contact", "account_holder", "iban", "bic", "created_at")
    search_fields = ("contact__username", "iban", "account_holder")
    list_filter = ("created_at",)
    ordering = ("contact",)  # Default ordering by contact

