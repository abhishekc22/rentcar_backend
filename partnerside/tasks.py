from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone
from buyerside.models import Booking


@shared_task
def send_mail_task():
    print("Mail sending.......")

    # Get all bookings with reserved status for the current date
    current_date = timezone.now().date()
    bookings = Booking.objects.filter(status="reserved")
    print(bookings, "jjjjjjjjjjjjjjjjjjjjjjjjjjj")

    for booking in bookings:
        # Extract relevant information from the booking
        email = booking.car.partner.user.email
        partner_email = email.split("-")[1]

        # Send a simple email without details
        email_subject = "Car Vacancy Details for {}".format(current_date)
        email_content = "Dear Buyer, there are vacant cars available today. Visit our website for more details."
        print("jjjjjjjjjjjjjjjjjjjjjjjjjjj")

        # Send the email
        send_mail(
            subject=email_subject,
            message=email_content,
            from_email="abhishek234264@gmail.com",
            recipient_list=[partner_email],
        )
        return "Mail has been sent........"
