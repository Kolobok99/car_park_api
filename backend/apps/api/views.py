from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.account import models as account_models
from apps.api import permissions
from apps.api import serializers
from apps.cars import models as cars_models
from apps.base import models as base_models
from services import filtration as custom_filters


class CarAPIViewSet(ModelViewSet):
    """APIViewSet: Машина"""

    queryset = cars_models.Car.objects.all()
    serializer_class = serializers.CarSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
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


class CarBrandAPIViewSet(ModelViewSet):
    """APIViewSet: CarBrand"""

    queryset = cars_models.CarBrand.objects.all()
    serializer_class = serializers.CarBrandSerializer
    permissions = [permissions.IsManager]


class UserAPIViewSet(ModelViewSet):
    """APIViewSet: User """

    queryset = account_models.UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_value_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsManagerOrOwnerObject]
        else:
            self.permission_classes = [permissions.IsManager]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.GET:
            serializer = self.serializer_class(custom_filters.filtration_user(request.GET), many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class DocumentTypesAPIViewSet(ModelViewSet):
    """APIViewSet: UserDocument """

    queryset = base_models.DocType.objects.all()
    serializer_class = serializers.DocTypeSerializer
    permissions = [permissions.IsManager]


class CarDocumentAPIViewSet(ModelViewSet):
    """APIViewSet: CarDocument """

    queryset = cars_models.CarDocument.objects.all()
    serializer_class = serializers.CarDocumentSerializer

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
    serializer_class = serializers.UserDocumentSerializer

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
    serializer_class = serializers.RepairRequestSerializer

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
    serializer_class = serializers.FuelCardSerializer
    lookup_field = 'number'

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