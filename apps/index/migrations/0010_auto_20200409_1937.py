# Generated by Django 3.0.3 on 2020-04-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0009_auto_20200406_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='next_inspection_hours',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
