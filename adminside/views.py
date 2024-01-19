from django.shortcuts import render
from accounts.models import *
from rest_framework import generics
from .serializer import Userlistserializer
from .permission import *
from partnerside.models import Rentcar
from partnerside.serializer import AddcarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import Carlistserializer, Bookingserializer, UserBlockSerializer
from buyerside.models import Booking
from rest_framework.generics import RetrieveAPIView
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from datetime import datetime
from buyerside.pagination import Carlistpagination
from .paginator import Admincarlistpagination


class Adminuserlist(generics.ListCreateAPIView):
    queryset = Customuser.objects.filter(role__in=["partner", "buyer"]).order_by(
        "-email"
    )
    serializer_class = Userlistserializer
    permission_classes = [is_admin]
    pagination_class = Carlistpagination


class Admincarlist(generics.ListCreateAPIView):
    queryset = Rentcar.objects.all()
    serializer_class = Carlistserializer
    permission_classes = [is_admin]
    pagination_class = Admincarlistpagination


class Carblockview(APIView):
    def put(self, request, car_id):
        try:
            car = Rentcar.objects.get(id=car_id)

            # Check if there are any active bookings for the car
            if Booking.objects.filter(car=car, is_cancelled=False).exists():
                return Response(
                    {"message": "Cannot unlist/list the car with active bookings."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            car.is_blocked = not car.is_blocked
            car.save()
            return Response(
                {"message": "Updated successfully."}, status=status.HTTP_201_CREATED
            )
        except Rentcar.DoesNotExist:
            return Response(
                {"message": "Car not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CarDetailsView(RetrieveAPIView):
    queryset = Rentcar.objects.all()
    serializer_class = Carlistserializer
    lookup_field = "id"


class Bookinglist(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = Bookingserializer
    permission_classes = [is_admin]
    pagination_class = Admincarlistpagination


class User_block(APIView):
    def put(self, request, id):
        try:
            user = Customuser.objects.get(id=id)

            # Toggle the is_blocked field
            user.is_blocked = not user.is_blocked
            user.save()

            message = "User blocked" if user.is_blocked else "User unblocked"
            return Response({"message": message}, status=status.HTTP_200_OK)
        except Customuser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AdminDashboard(APIView):
    def get(self, request, id):
        try:
            user = Customuser.objects.get(id=id)
            amount = user.wallet

            total_bookings = Booking.objects.all()
            print(len(total_bookings))

            total_booking_amount = (
                total_bookings.aggregate(total_amount=Sum("total_amount"))[
                    "total_amount"
                ]
                or 0
            )
            print(total_booking_amount)

            current_year = datetime.now().year

            monthly_sales_data = (
                total_bookings.filter(pickupdate__year=current_year)
                .annotate(month=ExtractMonth("pickupdate"))
                .values("month")
                .annotate(total_sales=Sum("total_amount"))
                .order_by("month")
            )
            print(monthly_sales_data, "9999999999")

            return Response(
                {
                    "message": "User found",
                    "wallet": amount,
                    "total_booking_amount": total_booking_amount,
                    "total_bookings": len(total_bookings),
                    "monthly_sales_data": list(
                        monthly_sales_data
                    ),  # Include monthly sales data in the response
                },
                status=status.HTTP_200_OK,
            )
        except Customuser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
