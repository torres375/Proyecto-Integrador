# Generated by Django 3.0.3 on 2020-04-09 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20200409_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightreport',
            name='aviation_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='flight_reports_aviation_units', to='index.TacticUnit'),
            preserve_default=False,
        ),
    ]