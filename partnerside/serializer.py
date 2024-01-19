# serializers.py
from buyerside.models import Booking
from rest_framework import serializers
from .models import Rentcar
from accounts.models import Parnterorofile, Customuser


class AddcarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rentcar
        fields = "__all__"

    def create(self, validated_data):
        # Retrieve the 'partner' data if present
        partner_data = validated_data.pop("partner", None)

        print(partner_data, "8888888888")
        # Create the Rentcar instance without the 'partner' field
        rentcar = Rentcar.objects.create(**validated_data)

        rentcar.partner = partner_data
        rentcar.save()
        return rentcar


class customserializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Parnterorofile
        fields = "__all__"
        depth = 1

    def get_email(self, obj):
        email = obj.user.email
        if email.startswith("partner-"):
            return email[len("partner-") :]
        return email

    def get_phone_number(self, obj):
        phone_number = obj.user.phone_number
        if phone_number.startswith("partner-"):
            return phone_number[len("partner-") :]
        return phone_number

    def get_username(self, obj):
        username = obj.user.username
        if username:
            return username


class Customserializerput(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["phone_number", "username"]


class Partnerserializerput(serializers.ModelSerializer):
    class Meta:
        model = Parnterorofile
        fields = ["partner_image"]

    def get_partner_image(self, obj):
        partner_image = obj.partner_image
        if partner_image:
            return partner_image
        else:
            return None


class Partnercarserializer(serializers.ModelSerializer):
    class Meta:
        model = Rentcar
        fields = "__all__"


class BuyerSerializer(serializers.Serializer):
    buyer_id = serializers.IntegerField()
    buyer_name = serializers.CharField()
    buyer_image = serializers.ImageField()


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["pickupdate", "returndate", "total_amount", "buyer", "car"]

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
