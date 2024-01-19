from rest_framework.permissions import BasePermission


class Isbuyer(BasePermission):
    def is_buyer(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "buyer"
        return False


class is_partner(BasePermission):
    def is_partner(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "partner"
        return False


class is_admin(BasePermission):
    def is_admin(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "admin"
        return False
