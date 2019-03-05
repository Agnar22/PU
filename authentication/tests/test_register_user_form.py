from django.test import TestCase, RequestFactory
from apartments.models import Apartment
from authentication.models import Profile
from authentication.forms import RegisterForm


class RegisterFormTest(TestCase):
    def test_form_no_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_form_valid_data(self):
        form = RegisterForm(data={
            'email': "test@test.test",
            'first_name': "Test",
            'last_name': "Test",
            'phone_number': 12345678,
            'password': "TestPassword"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

# python manage.py test authentication