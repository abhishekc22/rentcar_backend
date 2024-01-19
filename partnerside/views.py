# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Rentcar
from accounts.models import Parnterorofile, Customuser
from .serializer import (
    AddcarSerializer,
    customserializer,
    Partnerserializerput,
    Customserializerput,
    Partnercarserializer,
)
from buyerside.serializer import BookingSerializerall
from buyerside.models import Booking
from django.http import JsonResponse
from .serializer import BuyerSerializer
from datetime import date
from .serializer import BookingSerializer
from decimal import Decimal


class Addcarview(APIView):
    def post(self, request, partner_id):
        print(request.data)
        print(partner_id, "***************")
        partner = Parnterorofile.objects.filter(
            user__id=partner_id, user__is_blocked=False
        ).first()

        print(partner.id, "88888888888")

        request.data["partner"] = partner.id

        serializer = AddcarSerializer(data=request.data)
        print(
            request.data,
            "********************************8585**************************",
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Partner_profile(APIView):
    def get(self, request, parnter_id):
        user = Customuser.objects.get(id=parnter_id)
        print(user, "88888888888")
        partner = Parnterorofile.objects.filter(user=user).first()
        serializer = customserializer(partner)
        print(serializer.data, "***********")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, parnter_id):
        try:
            print(parnter_id, "hello")
            partner = Parnterorofile.objects.filter(user__id=parnter_id).first()
            print(partner, "***********")
            custom_serializer = Customserializerput(
                instance=partner.user, data=request.data, partial=True
            )
            partner_serializer = Partnerserializerput(
                instance=partner, data=request.data, partial=True
            )
            print("sdjbck")
            print(request.data)

            if partner_serializer.is_valid() and custom_serializer.is_valid():
                customser_instance = custom_serializer.save()
                partner_instance = partner_serializer.save()
                customser_instance.phone_number = (
                    "partner-" + custom_serializer._validated_data.get("phone_number")
                )
                customser_instance.save()
                data = {
                    "partner": Partnerserializerput(partner_instance).data,
                    "customer": Customserializerput(customser_instance).data,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                print("Partner Serializer Errors:", partner_serializer.errors)
                print("Custom Serializer Errors:", custom_serializer.errors)

                errors = {
                    "partner_errors": partner_serializer.errors,
                    "custom_erors": custom_serializer.errors,
                }
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"{str(e)}")


class Partnercar(generics.ListAPIView):
    serializer_class = Partnercarserializer

    def get(self, request, *args, **kwargs):
        partner_id = self.kwargs["partner_id"]
        user = Customuser.objects.filter(id=partner_id).first()
        partner = Parnterorofile.objects.filter(user=user).first()
        queryset = Rentcar.objects.filter(
            partner=partner, is_blocked=True, is_deleted=False
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class partnerbooking(generics.ListAPIView):
    serializer_class = BookingSerializerall

    def get_queryset(self):
        partner_id = self.kwargs["partner_id"]
        user = Customuser.objects.filter(id=partner_id).first()
        partner = Parnterorofile.objects.filter(user=user).first()
        buyer = Booking.objects.filter(car__partner=partner).order_by("-id")
        print(buyer, "888888888888888888888")
        return buyer


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class Buyer_get(APIView):
    def get(self, request, partnerid):
        try:
            partner = Parnterorofile.objects.get(user__id=partnerid)
            partner_cars = Rentcar.objects.filter(partner=partner)
            partner_bookings = Booking.objects.filter(car__in=partner_cars)
            print(partner_bookings, "++++++++++++++++")

            # Extract unique buyer information
            unique_buyers = set()
            buyer_data = []

            for booking in partner_bookings:
                buyer_id = booking.buyer.user.id
                buyer_name = booking.buyer.user.username
                buyer_image = (
                    booking.buyer.buyer_image
                )  # Adjust based on your actual field
                print(buyer_id, "---------")

                # Ensure uniqueness based on buyer_id
                if buyer_id not in unique_buyers:
                    unique_buyers.add(buyer_id)
                    buyer_data.append(
                        {
                            "buyer_id": buyer_id,
                            "buyer_name": buyer_name,
                            "buyer_image": buyer_image,
                        }
                    )
            print(buyer_data, "=============================")

            serializer = BuyerSerializer(buyer_data, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Parnterorofile.DoesNotExist:
            return JsonResponse({"error": "Partner not found"}, status=404)


class Deletecar(APIView):
    def delete(self, request, car_id):
        try:
            car = get_object_or_404(Rentcar, id=car_id)

            future_bookings_exist = Booking.objects.filter(
                car=car,
                returndate__gte=date.today(),
                status__in=["reserved", "running"],
            ).exists()

            if future_bookings_exist:
                return JsonResponse(
                    {"error": 'Car is booked in the future. Cannot "delete".'},
                    status=400,
                )

            car.is_deleted = True
            car.save()

            return JsonResponse({"success": "Car hidden successfully"}, status=201)

        except Rentcar.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class BookingRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print("Serializer Validation Error:", e)
            return Response(
                {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the status is being updated
        if "status" in request.data:
            new_status = request.data["status"]
            print("helooooooooooooooo")

            if new_status == "canceled":
                amount = Decimal(str(instance.total_amount))
                print(amount, "10101010")
                partner = amount * Decimal("0.75")
                admin = amount * Decimal("0.25")
                print(partner, admin, "********")

                buyer_wallet = instance.buyer.user
                partner_wallet = instance.car.partner.user
                print(partner_wallet, buyer_wallet)

                # Subtract partner amount from partner's wallet
                partner_wallet.wallet -= partner
                partner_wallet.save()

                # Subtract admin amount from admin's wallet
                admin_user = Customuser.objects.filter(role="admin").first()
                admin_user.wallet -= admin  # Corrected line
                admin_user.save()

                # Calculate buyer amount and add to buyer's wallet
                buyer_amount = partner + admin
                buyer_wallet.wallet += buyer_amount
                buyer_wallet.save()
                print(buyer_wallet, "=============")

                try:
                    # Your logic to refund money to the buyer's wallet
                    # buyer_wallet.refund(instance.total_amount)
                    # Make sure to replace 'refund' and 'total_amount' with your actual methods and fields
                    pass
                except Exception as e:
                    return Response(
                        {"error": "Failed to refund money"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            instance.status = new_status
            instance.save()

        return Response(serializer.data)
