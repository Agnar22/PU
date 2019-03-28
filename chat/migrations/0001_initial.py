from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_profile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time', models.DateField()),
                ('messager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messager', to='authentication.Profile')),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to='authentication.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(to='chat.Message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='person1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person1', to='authentication.Profile'),
        ),
        migrations.AddField(
            model_name='chat',
            name='person2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person2', to='authentication.Profile'),
        ),
    ]
