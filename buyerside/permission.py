from rest_framework.permissions import BasePermission


class Isbuyer(BasePermission):
    def is_buyer(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "buyer"
        return False
