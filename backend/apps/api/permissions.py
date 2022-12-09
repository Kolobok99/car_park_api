"""
CAR:
    менеджер        - ВСЕ
    владелец авто   - RETRIEVE, UPDATE, PART_UPDATE (свою машину)

DRIVER:
    менеджер        - ВСЕ
    владелец        - RETRIEVE, UPDATE, PART_UPDATE (свою модель)


AutoDoc:
    менеджер        - ВСЕ
    владелец        - RETRIEVE, UPDATE, PART_UPDATE, DESTROY (своих машин)

DriverDoc
    менеджер        - LIST, RETRIEVE, DESTROY
    владелец        - RETRIEVE, UPDATE, PART_UPDATE, DESTROY (свои доки)

FuelCards
    менеджер        - ВСЕ
    владелец        - RETRIEVE (cвою карту), UPDATE, PART_UPDATE, (баланс)

Applications
    менеджер        - LIST, RETRIEVE, CREATE
                      UPDATE ( свои
                               комментирование
                               изменение статуса
                               )
                      DELETE (свои)

    владелец        - (свои) RETRIEVE, CREATE, DESTROY
                      UPDATE (
                              type
                              urgency
                              description
                             )
                    -
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from apps.cars import models as cars_models

class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_manager():
            return True


class IsOwnerObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.owner == request.user:
            return True

    # def has_permission(self, request, view):
    #     return True


class IsManagerOrCarOwnerObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.is_manager()) or \
        obj.car.owner == request.user



class IsManagerOrOwnerObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager() or obj.owner == request.user:
            return True

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsManagerOrObjectIsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager() or obj == request.user:
            return True

    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsManagerObjectIsDocumentCarOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_manager() or obj.car.owner == request.user

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action == 'create' and request.data.get('car_reg_number', None):
                car_reg_number = request.data.get('car_reg_number').upper()
                try:
                    car = cars_models.Car.objects.get(registration_number=car_reg_number)
                    return request.user.is_manager() or request.user == car.owner
                except ObjectDoesNotExist:
                    return True
        return request.user.is_authenticated

        # if request.user.is_authenticated:
