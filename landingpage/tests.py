from django.test import TestCase

# Create your tests here:
from django.urls import reverse, resolve


class TestLandingPage(TestCase):
    def test_detail_url(self):
        path = reverse('landing-page')
        assert resolve(path).view_name == 'landing-page'