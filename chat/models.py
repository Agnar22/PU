from django.db import models

import datetime

from authentication.models import Profile


# Create your models here.
class Message(models.Model):
    content = models.TextField()
    messager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messager", null=True)
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reciever", null=True)
    time = models.TimeField()
    date = models.DateField(null=True)


class Chat(models.Model):
    messages = models.ManyToManyField(Message)
    person1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="person1", null=True)
    person2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="person2", null=True)
    last_message = models.TimeField(null=True)
    last_message_date = models.DateField(null=True)
