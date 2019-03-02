import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from authentication.models import Profile


class Contract(models.Model):
    contract_text = models.TextField()
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tenant", null=True)
    pending = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '' + str(self.start_date.strftime("%d.%m.%Y")) + ' - ' + \
               str(self.end_date.strftime("%d.%m.%Y"))


class Apartment(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=50)
    beds = models.IntegerField()
    apartment_age = models.IntegerField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    monthly_cost = models.PositiveIntegerField()
    vote_amount = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    contracts = models.ManyToManyField(Contract)
    image1 = ProcessedImageField(upload_to='apartments/',
                                 processors=[ResizeToFit(2000, 2000, False)],
                                 format='JPEG',
                                 options={'quality': 85})

    def __str__(self):
        return self.title

    def calculate_price(self, start_date, end_date):
        start_date = start_date.split('-')
        start_date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = end_date.split('-')
        end_date = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        delta = end_date - start_date
        apartment_price = round(self.monthly_cost / 30 * delta.days)

        return apartment_price

    def save(self, *args, **kwargs):
        if not self.title:
            self.vote_amount = 0
            self.rating = 0
        super().save(*args, **kwargs)
