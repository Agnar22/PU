# Generated by Django 2.1.5 on 2019-03-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20190312_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_message',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(),
        ),
    ]