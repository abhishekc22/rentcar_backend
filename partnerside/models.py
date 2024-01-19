from django.db import models
from accounts.models import Parnterorofile
from django.core.validators import MinValueValidator


# Create your models here.
class Rentcar(models.Model):
    partner = models.ForeignKey(Parnterorofile, on_delete=models.CASCADE)
    carname = models.CharField(max_length=20, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    enginetype = models.CharField(max_length=20, blank=False, null=False)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True)
    car_type = models.CharField(max_length=100, null=True, blank=True)
    is_blocked = models.BooleanField(default=False, blank=True, null=True)
    document = models.ImageField(blank=True, null=True)
    carimage1 = models.ImageField(blank=True, null=True)
    carimage2 = models.ImageField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.carname
