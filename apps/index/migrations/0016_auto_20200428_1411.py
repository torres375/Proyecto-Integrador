# Generated by Django 2.2.4 on 2020-04-28 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_auto_20200427_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightreport',
            name='civil_evacuations',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='crew_hours',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='dead_en',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='dead_pt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='fuel',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='kilos',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='machine_hours',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='pax',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='sick_en',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='sick_pt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='wounded_en',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='wounded_pt',
            field=models.IntegerField(default=0),
        ),
    ]
