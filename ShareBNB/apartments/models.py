from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.
class Apartment(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    beds = models.IntegerField()
    apartment_age = models.IntegerField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    monthly_cost = models.PositiveIntegerField()
    vote_amount = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    profile_picture = ProcessedImageField(upload_to='apartments/', processors =[ResizeToFit(2000, 2000,False)], format ='JPEG', options = {'quality': 85})




