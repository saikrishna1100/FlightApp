# Generated by Django 4.2.2 on 2023-06-29 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_business_fare_flight_fare_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='depart_day',
            new_name='departure_day',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='depart_time',
            new_name='departure_time',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='flight_adate',
            new_name='flight_arrival_date',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='flight_ddate',
            new_name='flight_destination_date',
        ),
    ]
