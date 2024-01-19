from rest_framework import serializers
from .models import *
from .models import Chat
from accounts.models import Customuser


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["message", "sender_username", "send_at"]

    def get_sender_username(self, obj):
        return obj.sender.username
