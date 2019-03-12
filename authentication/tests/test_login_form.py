from django.test import TestCase, RequestFactory
from apartments.models import Apartment
from authentication.models import Profile
from authentication.forms import LoginForm


class RegisterFormTest(TestCase):
    def test_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_form_valid_data(self):
        form = LoginForm(data={
            'email': "test@test.test",
            'password': "TestPassword"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

# python manage.py test authentication