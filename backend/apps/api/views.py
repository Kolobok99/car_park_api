from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import serializers as base_serializers
from apps.account import serializers as account_serializers
from apps.cars import serializers as cars_serializers

from apps.api import permissions

from services import filtration as custom_filters


class CarAPIViewSet(ModelViewSet):
    """APIViewSet: Машина"""

    queryset = cars_models.Car.objects.all()
    serializer_class = cars_serializers.CarSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrCarOwnerObject]
        elif self.action == 'confiscate':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(custom_filters.filtration_car(request.GET), many=True,
                                               context={'request': request})
        else:
            serializer = self.serializer_class(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)


    # @action(methods=['post'], detail=False)
    # def confiscate(self, request, *args, **kwargs):
    #     """
    #     Удаляет владельца у переданного списка карт
    #     """
    #     print(request.data)
    #     print(request.data.getlist('id'))
    #     print(account_models.UserModel.objects.get())
    #     return Response({"error": "формат!!!"})

class CarBrandAPIViewSet(ModelViewSet):
    """APIViewSet: CarBrand"""

    queryset = cars_models.CarBrand.objects.all()
    serializer_class = cars_serializers.CarBrandSerializer
    permission_classes = [permissions.IsManager, ]


class UserAPIViewSet(ModelViewSet):
    """APIViewSet: User """

    queryset = account_models.UserModel.objects.all()
    serializer_class = account_serializers.UserSerializer
    lookup_value_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        elif self.action == 'account_activation':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(custom_filters.filtration_user(request.GET), many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def account_activation(self, request, *args, **kwargs):

        user = self.queryset.filter(activation_code=request.POST.get('activation_code'))
        if user:
            user[0].is_active = True
            user[0].save()
            return Response({"success": "Аккаунт активирован"})
        else:
            return Response({"error": "Activation code is not valid"})


class DocumentTypesAPIViewSet(ModelViewSet):
    """APIViewSet: UserDocument """

    queryset = base_models.DocType.objects.all()
    serializer_class = base_serializers.DocTypeSerializer
    permission_classes = [permissions.IsManager, ]


class CarDocumentAPIViewSet(ModelViewSet):
    """APIViewSet: CarDocument """

    queryset = cars_models.CarDocument.objects.all()
    serializer_class = cars_serializers.CarDocumentSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(
                custom_filters.filtration_documents(cars_models.CarDocument, request.GET),
                many=True
            )
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class UserDocumentAPIViewSet(ModelViewSet):
    """APIViewSet: UserDocument """

    queryset = account_models.UserDocument.objects.all()
    serializer_class = account_serializers.UserDocumentSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsOwnerObject]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(
                custom_filters.filtration_documents(account_models.UserModel, request.GET),
                many=True
            )
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class RepairRequestAPIViewSet(ModelViewSet):
    """ APIViewSet: RepairRequest """

    queryset = cars_models.RepairRequest.objects.all()
    serializer_class = cars_serializers.RepairRequestSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsOwnerObject]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(custom_filters.filtration_reqs(request.GET), many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class CardsAPIViewSet(ModelViewSet):
    """APIViewSet: FuelCard """

    queryset = account_models.FuelCard.objects.all()
    serializer_class = account_serializers.FuelCardSerializer
    # lookup_field = 'number'

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsOwnerObject]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(custom_filters.filtration_reqs(request.GET), many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class NotificationAPIViewSet(ModelViewSet):
    """APIViewSet Notification"""

    queryset = account_models.Notification.objects.all()
    serializer_class = account_serializers.NotificationSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsManager]
        else:
            self.permission_classes = [permissions.IsOwnerObject]
        return super().get_permissions()