# Generated by Django 3.0.3 on 2020-03-20 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_auto_20200317_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightreport',
            name='crew',
        ),
        migrations.RemoveField(
            model_name='flightreport',
            name='id',
        ),
        migrations.AddField(
            model_name='flightreport',
            name='flight_order_id',
            field=models.CharField(default=0, max_length=100, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flightreport',
            name='risk_classification',
            field=models.CharField(choices=[('HIGH', 'RIESGO ALTO'), ('MED', 'RIESGO MEDIO'), ('LOW', 'RIESGO BAJO')], default='LOW', max_length=4),
        ),
        migrations.AddField(
            model_name='flightreport',
            name='route',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='flightreport',
            name='aviation_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight_reports_events', to='index.AviationEvent'),
        ),
    ]
