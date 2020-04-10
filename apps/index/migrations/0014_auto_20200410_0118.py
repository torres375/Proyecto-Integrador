# Generated by Django 3.0.3 on 2020-04-10 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_auto_20200409_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircrew',
            name='flight_reports',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crew_flight_report', to='index.FlightReport'),
        ),
    ]
