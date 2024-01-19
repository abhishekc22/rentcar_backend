from django.urls import path, include
from .views import *

urlpatterns = [
    path("Partnerlogin-api/", PartnerloginApi.as_view()),
    path("Buyerlogin-api/", BuyerLoginApi.as_view()),
    path("Buyer-signup/", Buyersignup.as_view()),
    path("partner-signup/", Partnersignup.as_view()),
    path("adminlogin-api/", Adminlogin.as_view()),
    path("buyer_google/", BuyerGoogleLogin.as_view()),
]
