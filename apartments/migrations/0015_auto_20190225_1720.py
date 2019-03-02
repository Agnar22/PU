# Generated by Django 2.1.5 on 2019-02-25 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0014_auto_20190225_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_owner', to='authentication.Profile'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='subtenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_subtenant', to='authentication.Profile'),
        ),
    ]