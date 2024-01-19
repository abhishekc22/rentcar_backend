from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Customuser(AbstractUser):
    Roles = (
        ("buyer", "Buyer"),
        ("partner", "Partner"),
        ("admin", "Admin"),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]
    role = models.CharField(max_length=10, choices=Roles, default="buyer")
    is_blocked = models.BooleanField(default=False, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    wallet = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # Add a wallet field

    def __str__(self):
        return self.email


class Buyerprofile(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    buyer_image = models.ImageField(blank=True, null=True)
    buyer_license_front = models.ImageField(blank=True, null=True)
    buyer_license_back = models.ImageField(blank=True, null=True)


class Parnterorofile(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    partner_image = models.ImageField(blank=True, null=True)


class Adminprofile(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
