# Generated by Django 3.0.3 on 2020-04-09 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_flightreport_minor_operative_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightreport',
            name='tactic_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight_reports_tactic_units', to='index.TacticUnit'),
        ),
    ]
