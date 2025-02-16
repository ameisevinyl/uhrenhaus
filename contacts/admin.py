from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, Address


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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Address.
    Allows listing, searching, and filtering addresses.
    """
    list_display = ("contact", "address_line_1", "city", "postal_code", "country", "is_residential")
    search_fields = ("contact__username", "address_line_1", "city", "postal_code")
    list_filter = ("country", "is_residential")
