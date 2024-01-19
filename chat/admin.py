from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "message",
        "is_read",
        "send_at",
        "thread_name",
    )
    search_fields = ("sender__username", "receiver__username", "message", "thread_name")
    list_filter = ("is_read", "send_at")
