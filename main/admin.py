
# Register your models here.
from django.contrib import admin
from .models import Tenants, Properties, Payments, Incidents


# Inline class for Payments in Properties
class PaymentInline(admin.TabularInline):
    model = Payments
    extra = 1  # This controls how many empty forms to display


# Customizing the Tenants Admin
class TenantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'adm_no')
    search_fields = ('name', 'email', 'phone', 'adm_no')
    list_filter = ('email',)  # You can add filters for other fields as well


# Customizing the Properties Admin
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('lot_no', 'tenant', 'area', 'price', 'available')
    list_filter = ('available',)
    search_fields = ('lot_no', 'tenant__name', 'tenant__email')
    inlines = [PaymentInline]


# Customizing the Payments Admin
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'lot_no', 'status', 'payment_amount', 'expected_date', 'payment_date', 'delays')
    list_filter = ('status', 'tenant')
    search_fields = ('tenant__name', 'lot_no__lot_no')
    readonly_fields = ('created_at', 'updated_at')  # You can add any fields that should be read-only


# Customizing the Incidents Admin
class IncidentsAdmin(admin.ModelAdmin):
    list_display = ('tenant_name', 'lot_no', 'description', 'is_utility', 'is_social', 'created_at')
    list_filter = ('is_utility', 'is_social')
    search_fields = ('tenant_name', 'lot_no', 'description')


# Register models with their corresponding admin classes
admin.site.register(Tenants, TenantsAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Incidents, IncidentsAdmin)

