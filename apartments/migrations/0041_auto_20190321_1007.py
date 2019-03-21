# Generated by Django 2.1.5 on 2019-03-21 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0040_auto_20190321_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='images',
        ),
        migrations.AddField(
            model_name='apartmentimage',
            name='image_for',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment'),
            preserve_default=False,
        ),
    ]