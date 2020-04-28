# Generated by Django 2.2.4 on 2020-04-27 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0014_auto_20200410_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightreport',
            name='observations',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='risk_classification',
            field=models.CharField(blank=True, choices=[('HIGH', 'RIESGO ALTO'), ('MED', 'RIESGO MEDIO'), ('LOW', 'RIESGO BAJO')], max_length=4, null=True),
        ),
    ]