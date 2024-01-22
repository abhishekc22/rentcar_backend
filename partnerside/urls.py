from django.urls import path, include
from .views import *


urlpatterns = [
    path("addcar/<int:partner_id>/", Addcarview.as_view(), name="addcar"),
    path(
        "partner_get/<int:parnter_id>/",
        Partner_profile.as_view(),
        name="partner_profile",
    ),
    path("partnercar/<int:partner_id>/", Partnercar.as_view(), name="partnercar"),
    path(
        "partnerbookings/<int:partner_id>/",
        partnerbooking.as_view(),
        name="partnerbookings",
    ),
    path("buyerget/<int:partnerid>/", Buyer_get.as_view(), name="buyerget"),
    path("deletecar/<int:car_id>/", Deletecar.as_view(), name="delete car"),
    path(
        "updating_status/<int:pk>/",
        BookingRetrieveUpdateView.as_view(),
        name="booking-retrieve-update",
    ),

    path('partnerdashboard/<int:partnerid>/',Partnerdashboard.as_view(),name='partnerdashboard'),
]
