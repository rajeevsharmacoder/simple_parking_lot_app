# Generated by Django 4.0.6 on 2022-07-19 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_app', '0004_alter_fruit_fruit_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fruit',
            options={'ordering': ['fruit_name'], 'verbose_name': 'home_fruit'},
        ),
    ]
