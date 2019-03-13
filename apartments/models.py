import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from multi_email_field.fields import MultiEmailField as MultiEmailField
from authentication.models import Profile


class Contract(models.Model):
    contract_text = models.TextField(null=True, blank=True)
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tenant", null=True)
    tenants = MultiEmailField(null=True, blank=True)
    pending = models.BooleanField()
    owner_approved = models.BooleanField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '' + str(self.start_date.strftime("%d.%m.%Y")) + ' - ' + \
               str(self.end_date.strftime("%d.%m.%Y"))

    def calculate_tenants(self):
        return len(self.tenants)

    def get_main_tenant(self):
        return self.tenants[0]


class Apartment(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50, default=None, null=True, blank=True)
    longitude = models.CharField(max_length=50, default=None, null=True, blank=True)
    beds = models.IntegerField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    monthly_cost = models.PositiveIntegerField()
    vote_amount = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    original_owner = models.EmailField(
        max_length=255,
        null=True,
        blank=True
    )
    contracts = models.ManyToManyField(Contract, blank=True)
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
