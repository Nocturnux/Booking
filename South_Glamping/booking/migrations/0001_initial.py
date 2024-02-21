# Generated by Django 4.2.7 on 2024-02-19 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_booking', models.DateField()),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('price', models.IntegerField()),
                ('status', models.CharField(default='Reservado', max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.customer')),
            ],
        ),
    ]
