from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.account.validators import balance_only_updatable_validator
from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import serializers as base_serializers
from apps.account import serializers as account_serializers
from apps.cars import serializers as cars_serializers

from apps.api import permissions
from apps.cars.validators import image_and_last_inspection_only_updatable_validator

from services import filtration as custom_filters
from services.filtration import CardFilter


class CarAPIViewSet(ModelViewSet):
    """APIViewSet: Машина"""

    queryset = cars_models.Car.objects.all()
    serializer_class = cars_serializers.CarSerializer
    lookup_field = 'registration_number'

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

    # @action(methods=['post'], detail=False)
    # def confiscate(self, request, *args, **kwargs):
    #     """
    #     Удаляет владельца у переданного списка карт
    #     """
    #     print(request.data)
    #     print(request.data.getlist('id'))
    #     print(account_models.UserModel.objects.get())
    #     return Response({"error": "формат!!!"})

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.is_manager():
            print('11111111')
            image_and_last_inspection_only_updatable_validator(data=request.data)
        return super().update(request, *args, **kwargs)

class CarBrandAPIViewSet(ModelViewSet):
    """APIViewSet: CarBrand"""

    queryset = cars_models.CarBrand.objects.all()
    serializer_class = cars_serializers.CarBrandSerializer
    permission_classes = [permissions.IsManager, ]
    lookup_field = 'title'

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

class UserAPIViewSet(ModelViewSet):
    """APIViewSet: User """

    queryset = account_models.UserModel.objects.all()
    serializer_class = account_serializers.UserSerializer
    lookup_field = 'email'
    # lookup_value_regex = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    lookup_value_regex = "[^/]+"

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsManagerOrObjectIsUser]
        elif self.action in ['account_activation', 'create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

    @action(methods=['post'], detail=False)
    def account_activation(self, request, *args, **kwargs):

        user = self.queryset.filter(activation_code=request.POST.get('activation_code'))
        if len(user) == 1:
            user.update(is_active=True)
            return Response({"success": "Account activated"})
        else:
            return Response({"error": "Account activation failed"})
class DocumentTypesAPIViewSet(ModelViewSet):
    """APIViewSet: Типы документов """

    queryset = base_models.DocType.objects.all()
    serializer_class = base_serializers.DocTypeSerializer
    permission_classes = [permissions.IsManager, ]


class CarDocumentAPIViewSet(ModelViewSet):
    """APIViewSet: CarDocument
     (с запрещенным изменением записи)"""

    queryset = cars_models.CarDocument.objects.all()
    serializer_class = cars_serializers.CarDocumentSerializer
    http_method_names = ['head', 'options', 'get', 'post', 'delete']

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsManagerObjectIsDocumentCarOwner]
        return super().get_permissions()



class UserDocumentAPIViewSet(ModelViewSet):
    """APIViewSet: UserDocument
    (с запрещенным изменением записи)"""

    queryset = account_models.UserDocument.objects.all()
    serializer_class = account_serializers.UserDocumentSerializer
    http_method_names = ['head', 'options', 'get', 'post', 'delete']

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [permissions.IsManager]
        elif self.action in ['retrieve']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        else:
            self.permission_classes = [permissions.IsOwnerObject]
        return super().get_permissions()



class RepairRequestAPIViewSet(ModelViewSet):
    """ APIViewSet: RepairRequest """

    queryset = cars_models.RepairRequest.objects.all()
    serializer_class = cars_serializers.RepairRequestSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        return super().get_permissions()


class RepairTypeAPIViewSet(ModelViewSet):
    """ APIViewSet: RepairRequest """

    queryset = cars_models.RepairType.objects.all()
    serializer_class = cars_serializers.RepairTypeSerializer
    permission_classes = [permissions.IsManager, ]


class CardAPIViewSet(ModelViewSet):
    """APIViewSet: FuelCard """

    queryset = account_models.FuelCard.objects.all()
    serializer_class = account_serializers.FuelCardSerializer
    lookup_field = 'number'
    filterset_class = CardFilter

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        return super().get_permissions()

    # def list(self, request, *args, **kwargs):
    #     if request.GET:
    #         serializer = self.serializer_class(custom_filters.filtration_cards(request.GET), many=True)
    #     else:
    #         serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.is_manager():
            balance_only_updatable_validator(data=request.data)
        return super().update(request, *args, **kwargs)

class NotificationAPIViewSet(ModelViewSet):
    """
        APIViewSet Notification
      (с запрещенным изменением записи)
    """

    queryset = account_models.Notification.objects.all()
    serializer_class = account_serializers.NotificationSerializer
    http_method_names = ['head', 'options', 'get', 'post', 'delete']

    def get_permissions(self):
        if self.action in ['retrieve', 'destroy']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

