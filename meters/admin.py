from django.contrib import admin
from .models import Unit, ConsumptionType, Meter, ConversionFactor

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Admin configuration for the Unit model."""
    list_display = ('name', 'location', 'size', 'parent_unit')
    search_fields = ('name', 'location')
    list_filter = ('parent_unit',)


@admin.register(ConsumptionType)
class ConsumptionTypeAdmin(admin.ModelAdmin):
    """Admin configuration for the ConsumptionType model."""
    list_display = ('name', 'unit')
    search_fields = ('name', 'unit')


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    """Admin configuration for the Meter model."""
    list_display = ('serial_number', 'consumption_type', 'unit', 'parent_meter')
    search_fields = ('serial_number', 'unit__name', 'consumption_type__name')
    list_filter = ('consumption_type', 'unit')

@admin.register(ConversionFactor)
class ConversionFactorAdmin(admin.ModelAdmin):
    """Admin configuration for the ConversionFactor model."""
    list_display = ('from_consumption_type', 'to_consumption_type', 'factor', 'start_date', 'end_date')
    search_fields = ('from_consumption_type__name', 'to_consumption_type__name')
    list_filter = ('start_date', 'end_date')
