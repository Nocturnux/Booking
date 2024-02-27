# Generated by Django 5.0.2 on 2024-02-27 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('payment_method', models.CharField(max_length=55)),
                ('status', models.CharField(max_length=25)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.booking')),
            ],
        ),
    ]
