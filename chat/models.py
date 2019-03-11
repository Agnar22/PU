from django.db import models

import datetime

from authentication.models import Profile

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    messager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messager", null=True)
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reciever", null=True)
    time = models.DateField()