from rest_framework import serializers
from accounts.models import Parnterorofile, Adminprofile, Customuser, Buyerprofile
from partnerside.models import Rentcar
from buyerside.models import Booking


class Userlistserializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["email", "username", "role", "id", "is_blocked"]


class partnerserializer(serializers.ModelSerializer):
    class Meta:
        model = Parnterorofile
        fields = "__all__"


class Carlistserializer(serializers.ModelSerializer):
    class Meta:
        model = Rentcar
        fields = "__all__"
        depth = 2


class Bookingserializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        depth = 4


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["is_blocked"]
