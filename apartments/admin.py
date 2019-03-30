from django.contrib import admin

from .models import Apartment, Contract, ApartmentImage


class ContractAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('contract_text', 'tenant', 'tenants', 'pending', 'owner_approved', 'start_date', 'end_date', 'review_made')

    class Meta:
        model = Contract


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating', 'city']
    fields = ('title', 'description', 'country', 'city', 'address', 'latitude', 'longitude', 'beds', 'rating', 'monthly_cost', 'original_owner', 'vote_sum', 'vote_amount', 'size', 'owner', 'contracts')

    class Meta:
        model = Apartment

class ApartmentImageAdmin(admin.ModelAdmin):
    list_display = ['image_for']
    fields = ('image', 'image_for')

    class Meta:
        model = ApartmentImage


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage, ApartmentImageAdmin)
admin.site.register(Contract, ContractAdmin)