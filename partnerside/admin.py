# admin.py
from django.contrib import admin
from .models import Rentcar


class RentcarAdmin(admin.ModelAdmin):
    list_display = (
        "partner",
        "carname",
        "location",
        "enginetype",
        "price",
        "car_type",
        "is_blocked",
    )


admin.site.register(Rentcar)
