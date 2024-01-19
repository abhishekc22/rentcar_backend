from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from accounts.models import Buyerprofile, Customuser, Adminprofile, Parnterorofile
from accounts.serializer import Signupserializer
from datetime import datetime
from .serializer import (
    Buyerprofileserializer,
    Customuserserializer,
    Singlecarserializer,
    BookingSerializerall,
)
from partnerside.models import Rentcar
from django.utils import timezone
from rest_framework import generics
from adminside.serializer import Carlistserializer
from .models import Booking
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from datetime import datetime
from decimal import Decimal
from .Signals import send_booking_notification
from .permission import *
from rest_framework.permissions import AllowAny


# Create your views here.


class Buyer_profile_edit(APIView):
    permission_classes = [Isbuyer]

    def get(self, request, user_id):
        user = get_object_or_404(Customuser, id=user_id)
        buyer = Buyerprofile.objects.filter(user=user).first()
        print(buyer)
        serializer = Buyerprofileserializer(buyer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = Buyerprofile.objects.filter(user__id=user_id).first()
        user_serializer = Customuserserializer(
            instance=user.user, data=request.data, partial=True
        )

        buyer_serializer = Buyerprofileserializer(user, data=request.data, partial=True)

        if user_serializer.is_valid() and buyer_serializer.is_valid():
            user_instance = user_serializer.save()
            buyer_instance = buyer_serializer.save()
            user_instance.email = "buyer-" + user_serializer.validated_data.get("email")
            user_instance.phone_number = "buyer-" + user_serializer.validated_data.get(
                "phone_number"
            )
            user_instance.save()

            data = {
                "buyer": Buyerprofileserializer(buyer_instance).data,
                "user": Customuserserializer(user_instance).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            errors = {
                "buyer_errors": buyer_serializer.errors,
                "user_errors": user_serializer.errors,
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class User_carlist(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Rentcar.objects.filter(is_blocked=True, is_deleted=False)
    serializer_class = Carlistserializer


class Siglepage(APIView):
    permission_classes = [Isbuyer]

    def get(self, request, car_Id):
        car = Rentcar.objects.get(id=car_Id)
        print(car, "---85858---")
        serializer = Singlecarserializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Bookingcar(APIView):
    permission_classes = [Isbuyer]

    def post(self, request):
        try:
            pickupdate = request.data.get("pickupdate")
            returndate = request.data.get("returndate")
            car_data = request.data.get("carId")
            buyer_id = request.data.get("user_id")
            print(pickupdate, returndate, car_data, buyer_id, "------------")

            # Validate date formats
            try:
                pickupdate = datetime.strptime(pickupdate, "%Y-%m-%d").date()
                returndate = datetime.strptime(returndate, "%Y-%m-%d").date()
                no_days = (returndate - pickupdate).days + 1

            except ValueError:
                return JsonResponse(
                    {"message": "Invalid date format. Please use YYYY-MM-DD."},
                    status=400,
                )

            # Assuming your Booking model has fields pickupdate, returndate, and car
            bookings_in_range = Booking.objects.filter(
                Q(pickupdate__range=[pickupdate, returndate])
                | Q(returndate__range=[pickupdate, returndate])
                | Q(pickupdate__lte=pickupdate, returndate__gte=returndate),
                car=car_data["id"],
            )

            car = Rentcar.objects.get(id=car_data.get("id"))
            price = car.price * no_days

            if pickupdate > returndate:
                return JsonResponse(
                    {"message": "Return date must be greater than pickup date."},
                    status=400,
                )

            if bookings_in_range.exists():
                return JsonResponse({"message": "Booking not available"}, status=400)
            else:
                new_booking = Booking(
                    pickupdate=pickupdate,
                    returndate=returndate,
                    car=car,
                    buyer=Buyerprofile.objects.filter(
                        user__id=buyer_id, user__is_blocked=False
                    ).first(),
                    total_amount=price,
                )
                serializer = Singlecarserializer(car)
                print(serializer.data, "---------------------")
                data = {
                    "message": "Booking created successfully",
                    "ownername": new_booking.car.partner.user.username,
                    "car_location": new_booking.car.location,
                    "owner_phonenumber": new_booking.car.partner.user.phone_number,
                    "buyer_name": new_booking.buyer.user.username,
                    "pickupdate": new_booking.pickupdate,
                    "returndate": new_booking.returndate,
                    "total_amount": new_booking.total_amount,
                    "document": serializer.data["document"],
                    "carimage": serializer.data["carimage1"],
                }
                return JsonResponse(data, status=201)

        except ValidationError as e:
            # Handle validation errors
            return JsonResponse({"error": str(e)}, status=400)

        except Exception as e:
            # Handle other exceptions
            print(e)
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from twilio.rest import Client


class Bookingpayment(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data, "----------")
            pickupdate = request.data.get("pickupdate")
            buyer_name = request.data.get("buyer_name")
            returndate = request.data.get("returndate")
            car_location = request.data.get("car_location")
            total_amount = Decimal(request.data.get("total_amount"))
            car = Rentcar.objects.filter(location=car_location).first()
            buyer = Buyerprofile.objects.filter(user__username=buyer_name).first()

            try:
                pickupdate = datetime.strptime(pickupdate, "%Y-%m-%d").date()
                returndate = datetime.strptime(returndate, "%Y-%m-%d").date()
                no_days = (returndate - pickupdate).days + 1

            except ValueError as e:
                print(f"Error converting dates: {e}")
                return JsonResponse(
                    {"message": "Invalid date format. Please use YYYY-MM-DD."},
                    status=400,
                )

            bookings_in_range = Booking.objects.filter(
                Q(pickupdate__range=[pickupdate, returndate])
                | Q(returndate__range=[pickupdate, returndate])
                | Q(pickupdate__lte=pickupdate, returndate__gte=returndate),
                car=car.id,
            )

            if pickupdate > returndate:
                return JsonResponse(
                    {"message": "Return date must be greater than pickup date."},
                    status=400,
                )

            if bookings_in_range.exists():
                return JsonResponse({"message": "Booking not available"}, status=400)

            else:
                new_booking = Booking(
                    pickupdate=pickupdate,
                    returndate=returndate,
                    car=car,
                    buyer=buyer,
                    total_amount=total_amount,
                    is_is_reserved=True,
                )
                new_booking.save()
                image = new_booking.car.carimage1

                # Trigger the email notification signal manually
                send_booking_notification(
                    sender=Booking, instance=new_booking, created=True
                )

                # in this   token and  sid  used  to authenticate  twilo( sandbox3rd party api)
                sid = "AC57b99cd11c54d16e6f6a529e672ea491"
                auth = "2e04618bc0e9944459e365a8d8ed8e38"

                client = Client(sid, auth)
                original_string = new_booking.buyer.user.phone_number
                print("looooooo77777oooooooo")

                #  then we  can send  only  the  messages
                # image_url = f'https://example.com/car_images/{new_booking.car.carimage1}'  # Replace with the actual logic to get the image UR
                whatsapp_message = f"New booking received!\nPickup Date: {new_booking.pickupdate}\nReturn Date: {new_booking.returndate}\nTotal Amount: {new_booking.total_amount}\nbuyername:{new_booking.buyer.user.username}\nphonenumber:{original_string[6:]}"
                try:
                    message = client.messages.create(
                        to="whatsapp:+919207475202",
                        from_="whatsapp:+14155238886",
                        body=whatsapp_message,
                    )
                    print("looooooooooooooo")
                except Exception as e:
                    print(f"Error sending WhatsApp notification: {e}")
                    print(f"Twilio Response: {e.msg}")

                # Update partner's wallet
                partner_user = new_booking.car.partner.user
                partner_user.wallet += new_booking.total_amount * Decimal("0.75")
                partner_user.save()

                # Update admin's wallet
                admin = Customuser.objects.filter(role="admin").first()
                admin.wallet += new_booking.total_amount * Decimal("0.25")
                admin.save()

                return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error in booking payment view: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# <<<<<<<<<<>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>


from django.conf import settings
import stripe
from rest_framework.response import Response
from django.shortcuts import redirect

# This is your test secret API key.

stripe.api_key = "sk_test_51OTJaXSAF3AtQFOEZcbPgmoT85USJJbCM3AQvW5Ka0ZJrNx05clrkYkxSvRu42uYFKnAXa0p6K5GkJFdgNdxFWWV003ZeFkWuy"


class Stripcheckout(APIView):
    def post(self, request):
        try:
            print(request.data, "***********************")
            total_amount = int(request.data["total_amount"])
            pickupdate = request.data.get("pickupdate")
            returndate = request.data.get("returndate")
            car_location = request.data.get("car_location")
            buyer_name = request.data.get("buyer_name")
            buyer = Buyerprofile.objects.filter(user__username=buyer_name).first()
            car = Rentcar.objects.filter(location=car_location).first()
            try:
                pickupdate = datetime.strptime(pickupdate, "%Y-%m-%d").date()
                returndate = datetime.strptime(returndate, "%Y-%m-%d").date()
                no_days = (returndate - pickupdate).days + 1

            except ValueError as e:
                print(f"Error converting dates: {e}")
                return JsonResponse(
                    {"message": "Invalid date format. Please use YYYY-MM-DD."},
                    status=400,
                )
            bookings_in_range = Booking.objects.filter(
                Q(pickupdate__range=[pickupdate, returndate])
                | Q(returndate__range=[pickupdate, returndate])
                | Q(pickupdate__lte=pickupdate, returndate__gte=returndate),
                car=car.id,
            )
            if bookings_in_range.exists():
                return JsonResponse({"message": "Booking not available"}, status=400)

            price = total_amount * 100
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "product_data": {
                                "name": "carway",
                            },
                            "unit_amount": price,
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                customer_email=buyer.user.email,  # Include customer's email
                cancel_url="http://localhost:5173/?canceled=true",
                success_url=f"http://localhost:5173/buyer/paymentsuccess?success=true&session_id={{CHECKOUT_SESSION_ID}}&pickupdate={pickupdate}&returndate={returndate}&car_location={car_location}&buyer_name={buyer_name}&total_amount={total_amount}",
            )

            return Response(status=status.HTTP_200_OK, data={"url": session.url})
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when creating Stripe Checkout session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class Buyer_bookedcar(generics.ListAPIView):
    serializer_class = BookingSerializerall
    permission_classes = [Isbuyer]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = Customuser.objects.filter(id=user_id).first()
        buyer = Buyerprofile.objects.filter(user=user).first()
        return Booking.objects.filter(buyer=buyer)


class Get_partner(APIView):
    def get(self, request, *args, **kwargs):
        byer_id = kwargs.get("byer_id")
        print(byer_id, "-----85---")
        try:
            buyer = Buyerprofile.objects.get(user__id=byer_id)
            bookings = Booking.objects.filter(buyer=buyer)
            # Get unique partners for the booked cars
            partner_ids = bookings.values_list(
                "car__partner__user__username", flat=True
            ).distinct()
            print(partner_ids, "-9696-----8----======================++++++++++")
            partners_data = []
            for partner_username in partner_ids:
                print(partner_username, "++++++++++++")
                partner = Parnterorofile.objects.filter(
                    user__username=partner_username
                ).first()

                if partner:
                    print(partner.user.id, "-----------*****************")
                    partners_data.append(
                        {
                            "id": partner.user.id,
                            "username": partner.user.username,
                            "image_url": str(partner.partner_image.url)
                            if partner.partner_image
                            else None,
                            # Add other fields you want to include
                        }
                    )

            serialized_data = {"partner_data": partners_data}

            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when creating Stripe Checkout session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


from datetime import datetime
from decimal import Decimal
from django.utils import timezone


class Cancelcar(APIView):
    def get(self, request, id):
        buyer_id = Booking.objects.get(id=id)

        try:
            booking_obj = Booking.objects.get(id=id)

            # Get the current date in the timezone of the booking (assuming the booking has a timezone field)
            current_date = timezone.now().date()

            # Ensure returndate is aware of the timezone
            returndate = booking_obj.returndate

            if returndate > current_date:
                booking_obj.status = "canceled"
                booking_obj.save()

                amount = Decimal(str(booking_obj.total_amount))
                print(amount, "**********")
                partner = amount * Decimal("0.75")
                print(partner, "----------")
                admin = amount * Decimal("0.25")
                print(admin, "--------")

                buyer = booking_obj.buyer.user
                partner_user = booking_obj.car.partner.user

                partner_user.wallet -= partner
                partner_user.save()

                admin_user = Customuser.objects.filter(role="admin").first()
                admin_user.wallet -= admin
                admin_user.save()

                buyer_amount = admin + partner
                buyer.wallet += buyer_amount
                buyer.save()
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong when canceling the order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BuyerWallet(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        buyer_id = self.kwargs["id"]
        print(buyer_id, "------------------222")
        print(buyer_id, "-----")
        try:
            buyer = Customuser.objects.get(id=buyer_id, role="buyer")
            print(buyer.wallet, "-------------------")
            return Response({"wallet_amount": buyer.wallet})
        except Customuser.DoesNotExist:
            return Response({"error": "Buyer not found"}, status=404)
