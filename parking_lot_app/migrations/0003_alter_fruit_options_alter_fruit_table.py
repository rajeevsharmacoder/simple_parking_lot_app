# Generated by Django 4.0.6 on 2022-07-19 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_app', '0002_rename_fruits_fruit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fruit',
            options={'ordering': ['-fruit_name'], 'verbose_name': 'home_fruit'},
        ),
        migrations.AlterModelTable(
            name='fruit',
            table='home_fruit',
        ),
    ]
