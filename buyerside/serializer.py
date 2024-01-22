from rest_framework import serializers
from accounts.models import Parnterorofile, Adminprofile, Customuser, Buyerprofile
from .models import Booking
from partnerside.models import Rentcar


class Buyerprofileserializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Buyerprofile
        fields = "__all__"
        depth = 2

    def get_email(self, obj):
        email = obj.user.email
        if email.startswith("buyer-"):
            return email[len("buyer-") :]
        return email

    def get_phone_number(self, obj):  # Corrected method name here
        phone_number = obj.user.phone_number
        if phone_number.startswith("buyer-"):
            return phone_number[len("buyer-") :]
        return phone_number


class Customuserserializer(serializers.ModelSerializer):
    buyer_image = serializers.FileField(source="buyerprofile.buyer_image")

    class Meta:
        model = Customuser
        fields = ("username", "email", "phone_number", "buyer_image")

    def update(self, instance, validated_data):
        # Handle the update for fields with dotted sources
        buyer_image_data = validated_data.pop("buyerprofile", {}).get(
            "buyer_image", None
        )
        if buyer_image_data:
            instance.buyerprofile.buyer_image = buyer_image_data
        # Update other fields
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        # Save the changes
        instance.save()
        return instance


class Singlecarserializer(serializers.ModelSerializer):
    class Meta:
        model = Rentcar
        fields = "__all__"
        depth = 2


class BookingSerializerall(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        depth = 4

class Carfilterserializer(serializers.ModelSerializer):
    class Meta:
        model=Rentcar
        fields= "__all__"
        depth = 2



