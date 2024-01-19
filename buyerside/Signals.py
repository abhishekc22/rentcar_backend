from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Booking
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Booking)
def send_booking_notification(sender, instance, **kwargs):
    if kwargs["created"]:
        partner_email = instance.car.partner.user.email
        subject = "New Booking Notification"

        # Load your HTML template
        html_content = render_to_string(
            "booking_notification_email.html", {"booking": instance}
        )
        text_content = strip_tags(
            html_content
        )  # This strips the html, leaving only the text

        # Send the email
        msg = EmailMultiAlternatives(
            subject, text_content, settings.EMAIL_HOST_USER, [partner_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
