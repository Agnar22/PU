# Generated by Django 2.1.5 on 2019-03-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_chat_last_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(to='chat.Message'),
        ),
    ]
