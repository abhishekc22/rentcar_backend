from rest_framework import serializers
from accounts.models import Parnterorofile, Adminprofile, Customuser, Buyerprofile


class Loginseralizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class Signupserializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class Googleserializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["email"]
