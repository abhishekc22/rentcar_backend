from django.db import models
from accounts.models import Buyerprofile, Adminprofile
from partnerside.models import Rentcar


class Booking(models.Model):
    buyer = models.ForeignKey(Buyerprofile, on_delete=models.CASCADE)
    car = models.ForeignKey(Rentcar, on_delete=models.CASCADE)
    pickupdate = models.DateField(blank=False, null=False)
    returndate = models.DateField(blank=False, null=False)
    total_amount = models.FloatField()
    is_cancelled = models.BooleanField(default=False)
    is_is_reserved = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ("canceled", "Canceled"),
        ("reserved", "Reserved"),
        ("running", "Running"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reserved")
