from django.urls import path, include
from .views import *


urlpatterns = [
    path("adminuserlist/", Adminuserlist.as_view()),
    path("carlist/", Admincarlist.as_view()),
    path("Carblock/<int:car_id>/", Carblockview.as_view(), name="Carblock"),
    path("cardetails/<int:id>/", CarDetailsView.as_view(), name="car-details"),
    path("booklist/", Bookinglist.as_view(), name="booking"),
    path("userblock/<int:id>/", User_block.as_view(), name="userblock"),
    path("admindash/<int:id>/", AdminDashboard.as_view(), name="admindashboard"),
]
