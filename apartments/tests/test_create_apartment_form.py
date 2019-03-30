from django.test import TestCase, RequestFactory
from apartments.models import Apartment
from apartments.forms import CreateApartmentForm


class ApartmentFormTest(TestCase):
    def test_form_no_data(self):
        form = CreateApartmentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)


    def test_form_no_image(self):
        form = CreateApartmentForm(data={
            'title': "Test",
            'description': "Test",
            'country': "Norge",
            'city':"Narvik",
            'address': "Kongens gate 2",
            'monthly_cost': 19000,
            'size': 300
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)