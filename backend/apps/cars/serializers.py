from rest_framework import serializers

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import validators as base_custom_validators
from apps.account import validators as account_custom_validators
from apps.cars import validators as cars_custom_validators


from apps.base import serializers as base_serializers
from apps.account import serializers as account_serializers

from services import services
from apps.polls import tasks


class CarBrandSerializer(serializers.ModelSerializer):
    """Сериализатор модели CarBrand"""

    class Meta:
        model = cars_models.CarBrand
        fields = "__all__"


class CarDocumentSerializer(serializers.ModelSerializer):

    type = serializers.PrimaryKeyRelatedField(label='тип', queryset=base_models.DocType.objects.filter(car_or_user='c'))

    class Meta:
        model = cars_models.CarDocument
        fields = "__all__"
        validators = [
            cars_custom_validators.CarOwnerOrManagerValidator,
            base_custom_validators.DateValidator,
        ]


class RepairRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = cars_models.RepairRequest
        fields = "__all__"
        validators = [
            cars_custom_validators.CarOwnerOrManagerValidator,
        ]


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор модели Car"""

    owner = serializers.HyperlinkedRelatedField(
            many=False,
            read_only=False,
            allow_null=True,
            view_name='user-detail',
            # lookup_field='email',
            # lookup_url_kwarg='email',
            queryset=account_models.UserModel.objects.filter(role='d'),
            label='Водитель'
        )
    docs = CarDocumentSerializer(many=True, read_only=True)
    reqs = RepairRequestSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['registration_number'] = validated_data['registration_number'].upper()
        return super().create(validated_data)

    class Meta:
        model = cars_models.Car
        fields = [
            'registration_number',
            'brand',
            'region_code',
            'last_inspection',
            'image',
            'owner',
            'image',
            'docs',
            'reqs',
        ]
        read_only_fields = ['docs', 'reqs']
        extra_kwargs = {
            'registration_number': {'validators': [cars_custom_validators.CarRegistrationNumberValidator]},
            'region_code': {'validators': [cars_custom_validators.CarRegionCodeValidator]},
        }