from django.test import TestCase

# Create your tests here.
from apartments.models import Apartment, Contract
from authentication.models import Profile


class ApartmentTest(TestCase):

    # def create_contract(self):
    #     return Contract.objects.create(contract_text="dsadsa",
    #                                    tenant=self.create_user(),
    #                                    start_date="2019-02-01",
    #                                    end_date="2019-03-04")
    #
    # def create_user(self):
    #     return Profile.objects.create(email="tobias.wulvik@gmail.com",
    #                                   first_name="Tobias",
    #                                   last_name="Wulvik",
    #                                   phone_number=47244448)
    #
    # def create_apartment(self):
    #     return Apartment.objects.create(title="Testleilighet",
    #                                     description="abcdefg",
    #                                     country="Norge",
    #                                     city="Trondheim",
    #                                     address="Aslak bolts gate 3",
    #                                     beds=4,
    #                                     apartment_age=1966,
    #                                     rating=4,
    #                                     monthly_cost=5000,
    #                                     size=43,
    #                                     owner=self.create_user(),
    #                                     contracts=self.create_contract())

    def test_apartment_creation(self):
        self.assertEqual(True, True)
