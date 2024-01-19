from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "car",
        "pickupdate",
        "returndate",
        "total_amount",
        "is_cancelled",
        "status",
    )
    search_fields = (
        "buyer__username",
        "car__car_name",
    )  # Adjust these fields based on your actual model structure


admin.site.register(Booking, BookingAdmin)
