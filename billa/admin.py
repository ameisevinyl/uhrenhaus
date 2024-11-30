from django.contrib import admin
from .models import Tenant, Unit, RentalContract, Rent


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    fieldsets = (
        (None, {'fields': ('username', 'name', 'nickname', 'email', 'billing_address', 'is_staff', 'is_active')}),
    )
    list_display = ('username', 'name', 'nickname', 'email', 'is_staff')
    search_fields = ('username', 'name', 'nickname', 'email')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'size', 'parent_unit')
    search_fields = ('name', 'location')
    list_filter = ('parent_unit',)


@admin.register(RentalContract)
class RentalContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'tenant', 'unit')
    search_fields = ('tenant__username', 'unit__name')


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        'rental_contract', 'start_date', 'end_date', 
        'net_rent', 'vat_rate', 'vat_amount', 'gross_rent', 'monthly_advance'
    )
    list_filter = ('start_date', 'end_date', 'rental_contract')
    search_fields = ('rental_contract__tenant__username', 'rental_contract__unit__name')
