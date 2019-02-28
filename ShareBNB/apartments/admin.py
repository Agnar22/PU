from django.contrib import admin

from .models import Apartment, Contract


class ContractAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('contract_text', 'tenant', 'pending'','start_date', 'end_date')

    class Meta:
        model = Contract


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating', 'city']
    fields = ('title', 'description', 'country', 'city', 'address', 'beds', 'apartment_age', 'rating', 'monthly_cost', 'vote_amount', 'size', 'image1', 'owner', 'contracts')

    class Meta:
        model = Apartment


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Contract, ContractAdmin)