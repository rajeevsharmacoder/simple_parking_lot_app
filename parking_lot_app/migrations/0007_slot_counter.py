# Generated by Django 4.0.6 on 2022-07-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_app', '0006_parking_slot_delete_fruit'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='counter',
            field=models.BigIntegerField(null=True),
        ),
    ]