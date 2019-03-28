import datetime

from django.test import TestCase, RequestFactory

from django.urls import reverse
from faker import Faker
from mixer.backend.django import mixer

from apartments.models import Apartment, Contract
from apartments.views import apartment_detail, apartments
from authentication.models import Profile


class ApartmentURLTest(TestCase):
    # def test_apartment_list(self):
    #     path = '/apartments/?location=Trondheim&start_date=2019-03-01&end_date=2019-04-01&guests=1'
    #     request = RequestFactory().get(path)
    #     request.content_params
    #     response = apartments(request)
    #
    #     self.assertEqual(response.status_code, 200)

    def test_apartment_detail(self):
        apartment = mixer.blend(Apartment)
        pk = apartment.pk
        start_date = '2019-03-19'
        end_date = '2019-04-19'
        path = reverse('apartment-detail', kwargs={'apartment_id': pk, 'start_date': start_date, 'end_date': end_date})
        request = RequestFactory().get(path)
        response = apartment_detail(request, pk, start_date, end_date)

        self.assertEqual(response.status_code, 200)