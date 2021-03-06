# Generated by Django 3.0.3 on 2020-05-10 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedHourMajorOperationAircraftModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_hours', models.FloatField()),
                ('aircraft_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_aircraft_model', to='index.AirCraftModel')),
                ('major_operative_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_major_operative_unit', to='index.MajorOperativeUnit')),
            ],
        ),
    ]
