# Generated by Django 3.0.3 on 2020-04-09 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_flightreport_aviation_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightreport',
            name='minor_operative_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight_reports_minor_operative_units', to='index.MinorOperativeUnit'),
        ),
    ]
