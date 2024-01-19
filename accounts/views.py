from django.shortcuts import render
from .serializer import *
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from buyerside.permission import *


# Create your views here
# parnterlogin


class PartnerloginApi(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Loginseralizer(data=data)

            if serializer.is_valid():
                email = "partner-" + serializer.data["email"]
                password = serializer.data["password"]

                user = authenticate(email=email, password=password)

                if user is None:
                    data = {
                        "message": "Invalid credentials or user is blocked.",
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "partnername": user.username,
                    "patrner_id": user.id,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )
        except Exception as e:
            print(e)


from rest_framework.permissions import AllowAny


# buyerlogin view
class BuyerLoginApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            print(data)
            serializer = Loginseralizer(data=data)
            print(serializer, "-------------------")
            if serializer.is_valid():
                email = "buyer-" + serializer.data["email"]
                password = serializer.data["password"]
                user = authenticate(email=email, password=password)
                print(user, "-----------")

                if user is None:
                    data = {
                        "message": "Invalid credentials or user is blocked.",
                    }
                    print("data", data)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "buyername": user.username,
                    "buyer_id": user.id,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )
        except Exception as e:
            print(e)


# buyer signup
class Buyersignup(APIView):
    def post(self, request):
        print("heloooo")
        serializer = Signupserializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            buyername = (user_data.get("username"),)
            user = Customuser(
                email="buyer-" + user_data.get("email"),
                role="buyer",
                phone_number="buyer-" + user_data.get("phone_number"),
                username=user_data.get("username"),
            )

            user.set_password(user_data.get("password"))
            user.save()

            # Assuming Buyerprofile model is defined and related to Customuser
            Buyerprofile.objects.create(user=user)

            return Response(
                {"messages": "Account created successfully.", "buyernames": buyername},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# partner signup
class Partnersignup(APIView):
    def post(self, request):
        print(request.data, "8989898")
        serializer = Signupserializer(data=request.data)
        print(serializer, "875656565656")

        if serializer.is_valid():
            print("hi............")

            user_data = serializer.validated_data
            print("ppppppppppppppppp", user_data)
            partnername = user_data.get("username")
            user = Customuser(
                email="partner-" + user_data.get("email"),
                role="partner",
                phone_number="partner-" + user_data.get("phone_number"),
                username=user_data.get("username"),
            )
            user.set_password(user_data.get("password"))
            user.save()
            Parnterorofile.objects.create(user=user)
            return Response(
                {
                    "message": "Account created successfully.",
                    "partnername": partnername,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# admindside
class Adminlogin(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data, "88888888888")
            serializer = Loginseralizer(data=data)
            print(serializer, "5252")
            if serializer.is_valid():
                email = serializer.data["email"]
                password = serializer.data["password"]
                admin = Customuser.objects.filter(role="admin")
                if admin:
                    user = authenticate(email=email, password=password)
                    print(user, "767676767676")

                if user is None:
                    data = {"message": "invalid credential"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role,
                    "email": user.email,
                    "admin_id": user.id,
                    "adminname": user.username,
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)
            # Properly handle the exception, e.g., log it or return an error response.
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BuyerGoogleLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Googleserializer(data=data)

            if serializer.is_valid():
                email = "buyer-" + data.get("email")
                # Filter by the correct email variable
                buyer = Customuser.objects.filter(email=email).first()

                if buyer:
                    buyer_id = buyer.id
                    print(buyer_id, "*+++++++++++++++++*")

                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(buyer)
                    data = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "buyername": buyer.username,
                        "buyer_id": buyer.id,
                    }
                    return Response(data, status=status.HTTP_201_CREATED)

                else:
                    # Handle the case where no user with the specified email is found
                    return Response(
                        {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                    )

            else:
                # Handle the case where the serializer is not valid
                print("Serializer is not valid:", serializer.errors)
                return Response(
                    {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            # Handle other exceptions
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
