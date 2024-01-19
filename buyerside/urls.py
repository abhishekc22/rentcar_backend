from django.urls import path, include
from .views import *


urlpatterns = [
    path("buyerprofile_edit/<int:user_id>/",Buyer_profile_edit.as_view(),name="buyerprofile_edit"),
    path("user_carlist/", User_carlist.as_view(), name="user_carlist"),
    path("singlepage/<int:car_Id>/", Siglepage.as_view(), name="singlepage"),
    path("booking/", Bookingcar.as_view(), name="booking"),
    path("bookingpayment/", Bookingpayment.as_view(), name="bookingpayment"),
    path("payment/", Stripcheckout.as_view(), name="payment"),
    path("buyerbooking/<int:user_id>/", Buyer_bookedcar.as_view(), name="buyerbooking"),
    path("get_partner/<int:byer_id>/", Get_partner.as_view(), name="get_partner"),
    path("cancel_order/<int:id>/", Cancelcar.as_view(), name="cancelorder"),
    path("wallet/<int:id>/", BuyerWallet.as_view(), name="wallet"),
]
