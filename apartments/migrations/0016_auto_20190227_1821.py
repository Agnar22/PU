# Generated by Django 2.1.5 on 2019-02-27 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0015_auto_20190225_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='subtenant',
        ),
        migrations.AlterField(
            model_name='contract',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile'),
        ),
    ]