# Generated by Django 3.0.3 on 2020-04-06 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20200320_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightreport',
            name='observations',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='route',
            field=models.CharField(max_length=1000),
        ),
    ]
