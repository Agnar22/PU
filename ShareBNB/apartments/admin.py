from django.contrib import admin

# Register your models here.
from .forms import CreateApartmentForm
from .models import Apartment


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    form = CreateApartmentForm
    class Meta:
        model = Apartment

admin.site.register(Apartment, ApartmentAdmin)