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

from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_manager():
            return True


class IsManagerOrOwnerObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager() or obj.car.owner == request.user:
            return True


class IsOwnerObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.owner == request.user:
            return True

    def has_permission(self, request, view):
        return True


# class IsManagerOrOwner(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if obj.owner == request.user or request.user.is_manager():
#              return True
#     def has_permission(self, request, view):
#         return True
#
#
#
#
# class IsManagerOrThisUser(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if obj == request.user or request.user.is_manager():
#             return True
#
#
# class IsOwnerOnly(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if obj.owner == request.user:
#             return True