from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Unit, ConsumptionType, Meter, ConversionFactor, MeterReading, Expense


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "size", "parent_unit", "created_at", "updated_at")
    search_fields = ("name", "location")
    list_filter = ("created_at", "updated_at")


@admin.register(ConsumptionType)
class ConsumptionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ("label", "serial_number", "consumption_type", "unit", "install_date", "deinstall_date", "created_at", "updated_at")
    search_fields = ("label", "serial_number")
    list_filter = ("install_date", "deinstall_date", "created_at", "updated_at")


@admin.register(ConversionFactor)
class ConversionFactorAdmin(admin.ModelAdmin):
    list_display = ("from_consumption_type", "to_consumption_type", "factor", "start_date", "end_date", "created_at", "updated_at")
    list_filter = ("start_date", "end_date", "created_at", "updated_at")


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ("meter", "reading_date", "value", "user", "is_estimated", "photo_preview", "created_at", "updated_at")
    list_filter = ("reading_date", "is_estimated", "created_at", "updated_at")
    search_fields = ("meter__label", "user__username")

    readonly_fields = ("photo_preview", "created_at", "updated_at")

    def photo_preview(self, obj):
        """Show a preview of the uploaded meter reading photo."""
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.photo.url)
        return "(No photo)"

    photo_preview.short_description = "Photo Preview"

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "meter", "supplier", "invoice_date", "total_cost", "vat_rate", "consumption")
    search_fields = ("invoice_number", "supplier__username", "meter__label")
    list_filter = ("invoice_date", "meter", "supplier")

    readonly_fields = ("total_cost", "consumption")  # ✅ Ensure calculated fields are read-only
