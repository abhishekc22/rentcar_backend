from django.db import models
from accounts.models import Customuser
from django.utils import timezone

# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(
        Customuser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        Customuser, on_delete=models.CASCADE, related_name="recieved_messages"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    send_at = models.DateTimeField(auto_now_add=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    class Meta:
        ordering = ["send_at"]
