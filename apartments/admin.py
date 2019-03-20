from django.contrib import admin

from .models import Apartment, Contract, ApartmentImage


class ImageAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('mainimage', 'image_for')

    class Meta:
        model = ApartmentImage

class ContractAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('contract_text', 'tenant', 'tenants', 'pending', 'owner_approved', 'start_date', 'end_date')

    class Meta:
        model = Contract


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating', 'city']
    fields = ('title', 'description', 'country', 'city', 'address', 'latitude', 'longitude', 'beds', 'apartment_age', 'rating', 'monthly_cost', 'original_owner', 'vote_amount', 'size', 'image1', 'owner', 'contracts')

    class Meta:
        model = Apartment


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ApartmentImage, ImageAdmin)