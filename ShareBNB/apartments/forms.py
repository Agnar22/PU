from django import forms
from django.core.exceptions import ValidationError

from .models import Apartment


class CreateApartmentForm(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = [
            'title',
            'description',
            'country',
            'city',
            'address',
            'beds',
            'apartment_age',
            'rating',
            'monthly_cost',
            'vote_amount',
            'size',
            'profile_picture'
        ]

    def clean_image(self):
        image = self.cleaned_data.get('profile_picture', False)
        if image:
            if image.size > 20*1024*1024:
                raise ValidationError("Image file too large ( > 20mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")