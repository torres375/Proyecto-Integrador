# Generated by Django 3.0.3 on 2020-03-09 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aviationevent',
            old_name='minicipality',
            new_name='municipality',
        ),
    ]