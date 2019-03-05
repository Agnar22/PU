from django.test import TestCase, RequestFactory

from apartments.models import Apartment


class ApartmentModelTest(TestCase):
    def setUp(self):
        self.apartment1 = Apartment.objects.create(
            title="TestApartment",
            country="Norge",
            city="Trondheim",
            address="Kongens gate 8",
            beds=4,
            apartment_age=19,
            rating=4,
            monthly_cost=10000,
            vote_amount=140,
            size=100
        )


    def test_calculate_price(self):
        price1 = self.apartment1.calculate_price("2019-01-01", "2019-01-16")
        price2 = self.apartment1.calculate_price("2019-03-11", "2019-04-16")
        price3 = self.apartment1.calculate_price("2019-04-19", "2019-07-16")
        price4 = self.apartment1.calculate_price("2019-02-27", "2019-09-16")
        price5 = self.apartment1.calculate_price("2018-08-04", "2019-05-16")
        price6 = self.apartment1.calculate_price("2019-07-09", "2019-12-16")

        self.assertEqual(price1, 5000)
        self.assertEqual(price2, 12000)
        self.assertEqual(price3, 29333)
        self.assertEqual(price4, 67000)
        self.assertEqual(price5, 95000)
        self.assertEqual(price6, 53333)

    def test_to_string(self):
        self.assertEqual(self.apartment1.__str__(), self.apartment1.title)



#python manage.py test apartments