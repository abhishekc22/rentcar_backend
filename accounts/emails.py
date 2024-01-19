from django.core.mail import send_mail
import random
from django import settings


def send_otp_via_email(email):
    subject = "your  account verification email"
    otp = random.randint(1000, 999)
    message = f"Your otp is {otp}"
    email_form = settings.EMAIL_HOST
    send_mail(subject, message, email_form, [email])
