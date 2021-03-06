# Generated by Django 2.1.5 on 2019-03-30 12:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import multi_email_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100000)),
                ('country', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('longitude', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('beds', models.IntegerField()),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('monthly_cost', models.PositiveIntegerField()),
                ('vote_sum', models.PositiveIntegerField(default=0)),
                ('vote_amount', models.PositiveIntegerField(default=0)),
                ('size', models.PositiveIntegerField()),
                ('original_owner', models.EmailField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='apartments/')),
                ('image_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_text', models.TextField(blank=True, null=True)),
                ('tenants', multi_email_field.fields.MultiEmailField(blank=True, null=True)),
                ('pending', models.BooleanField()),
                ('owner_approved', models.BooleanField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('review_made', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to='authentication.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='contracts',
            field=models.ManyToManyField(blank=True, to='apartments.Contract'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile'),
        ),
    ]
