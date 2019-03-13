# Generated by Django 2.1.5 on 2019-03-12 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20190312_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_message',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(null=True, to='chat.Message'),
        ),
    ]