# Generated by Django 4.2 on 2023-04-09 18:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.DateTimeField()),
                ('num_of_people', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('is_reserved', models.BooleanField(default=False)),
                ('campsite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_channel.campsite')),
            ],
            options={
                'unique_together': {('time_slot', 'campsite')},
            },
        ),
    ]
