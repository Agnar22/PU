from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from authentication.models import Profile


class Contract(models.Model):
    contract_text = models.TextField()
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE)
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
    beds = models.IntegerField()
    apartment_age = models.IntegerField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    monthly_cost = models.PositiveIntegerField()
    vote_amount = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField()
    image1 = ProcessedImageField(upload_to='apartments/', processors =[ResizeToFit(2000, 2000,False)], format ='JPEG', options = {'quality': 85})
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    contracts = models.ManyToManyField(Contract)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.vote_amount = 0
            self.rating = 0
        super().save(*args, **kwargs)
