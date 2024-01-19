from django.contrib import admin
from .models import Customuser, Buyerprofile, Parnterorofile, Adminprofile


class CustomuserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role", "is_blocked", "phone_number", "wallet")
    search_fields = ("email", "username", "phone_number")


class BuyerprofileAdmin(admin.ModelAdmin):
    list_display = ("user", "buyer_image", "buyer_license_front", "buyer_license_back")


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = "user"


admin.site.register(Customuser, CustomuserAdmin)
admin.site.register(Buyerprofile, BuyerprofileAdmin)
admin.site.register(Parnterorofile)
admin.site.register(Adminprofile)
