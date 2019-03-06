from django import forms

from .models import Apartment


class CreateApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateApartmentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autocomplete'] = "off"
        self.fields['title'].widget.attrs['placeholder'] = "."

        self.fields['description'].widget.attrs['autocomplete'] = "off"
        self.fields['description'].widget.attrs['placeholder'] = "."

        self.fields['address'].widget.attrs['autocomplete'] = "street-address"
        self.fields['address'].widget.attrs['placeholder'] = "."

        self.fields['city'].widget.attrs['autocomplete'] = "address-level-2"
        self.fields['city'].widget.attrs['placeholder'] = "."

        self.fields['country'].widget.attrs['autocomplete'] = "country-name"
        self.fields['country'].widget.attrs['placeholder'] = "."

        self.fields['beds'].widget.attrs['placeholder'] = "."

        self.fields['apartment_age'].widget.attrs['placeholder'] = "."

        self.fields['monthly_cost'].widget.attrs['placeholder'] = "."

        self.fields['size'].widget.attrs['placeholder'] = "."

        self.fields['original_owner'].widget.attrs['placeholder'] = "."
        self.fields['original_owner'].required = False

    class Meta:
        model = Apartment
        fields = [
            'title',
            'description',
            'address',
            'city',
            'country',
            'beds',
            'apartment_age',
            'monthly_cost',
            'size',
            'original_owner',
            'image1',
        ]
