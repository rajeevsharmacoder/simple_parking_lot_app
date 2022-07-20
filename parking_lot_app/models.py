from django.db import models

# Create your models here.


class Slot(models.Model):
    two_wheeler_count = models.IntegerField(default=20)
    four_wheeler_count = models.IntegerField(default=20)
    counter = models.BigIntegerField(null=True)


class Parking(models.Model):
    in_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False)

    out_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    class VehicleType(models.TextChoices):
        TWO_WHEELER = '2-WHEELER'
        FOUR_WHEELER = '4-WHEELER'

    vehicle_type = models.CharField(
        max_length=9,
        choices=VehicleType.choices,
        default=VehicleType.TWO_WHEELER
    )

    amount = models.FloatField(null=True, blank=True)

    amount_received = models.BooleanField(default=False)

    reference_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.reference_id + " : " + self.vehicle_type

    class Meta:
        db_table = 'parking'
        ordering = ['reference_id']
        unique_together = [['reference_id', 'vehicle_type']]
        verbose_name = "parking"
