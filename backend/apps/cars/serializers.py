import datetime

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import validators as base_custom_validators
from apps.cars import validators as cars_custom_validators
from apps.account import validators as account_custom_validators

from services.services import get_value_by_instance_or_from_validate_data

class CarBrandSerializer(serializers.ModelSerializer):
    """Сериализатор модели CarBrand"""

    class Meta:
        model = cars_models.CarBrand
        fields = "__all__"


class CarDocumentSerializer(serializers.ModelSerializer):

    car_reg_number = serializers.CharField(label='Номер машины:', write_only=True, validators=[cars_custom_validators.CarExistValidator])
    type = serializers.PrimaryKeyRelatedField(label='тип', queryset=base_models.DocType.objects.filter(car_or_user='c'))
    def create(self, validated_data):

        validated_data['car_reg_number'] = validated_data['car_reg_number'].upper()
        validated_data['car'] = cars_models.Car.objects.get(registration_number=validated_data.pop('car_reg_number'))
        return super().create(validated_data)


    class Meta:
        model = cars_models.CarDocument
        fields = [
            'id',
            'car',
            'car_reg_number',
            'type',
            'file',
            'start_date',
            'end_date',

        ]
        validators = [
            # cars_custom_validators.CarOwnerOrManagerValidator,
            base_custom_validators.DocumentDateValidator,
        ]
        extra_kwargs = {
            'car': {'read_only': True},
        }

class RepairTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = cars_models.RepairType
        fields = "__all__"


class RepairRequestSerializer(serializers.ModelSerializer):

    type_title = serializers.CharField(label='Название типа', write_only=True, validators=[cars_custom_validators.TypeOfRepairExistValidator])
    engineer_email = serializers.EmailField(label='Почта механика', required=False, write_only=True, validators=[account_custom_validators.EngineerExistValidator])
    car_reg_number = serializers.CharField(label='Номер авто', write_only=True, validators=[cars_custom_validators.CarExistValidator])
    owner_hidden = serializers.HiddenField(default=serializers.CurrentUserDefault())

    status_display = serializers.ChoiceField(source='get_status_display', choices=cars_models.RepairRequest.STATUS_CHOISES)
    owner = serializers.StringRelatedField(many=False)
    type = serializers.StringRelatedField(many=False)
    engineer = serializers.StringRelatedField(many=False)
    car = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='car-detail',
        lookup_field='registration_number'
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_active'] = 'ДА' if instance.is_active else 'НЕТ'
        representation['end_date'] = instance.end_date.strftime("%d-%m-%Y")
        return representation

    def create(self, validated_data):

        today = datetime.datetime.today()

        validated_data['type'] = cars_models.RepairType.objects.get(title=validated_data.pop('type_title'))
        validated_data['owner'] = account_models.UserModel.objects.get(email=validated_data.pop('owner_hidden'))
        validated_data['engineer'] = account_models.UserModel.objects.filter(email=validated_data.pop('engineer_email')).first()
        validated_data['car'] = cars_models.Car.objects.get(registration_number__iexact=validated_data.pop('car_reg_number'))

        validated_data['end_date'] = today + datetime.timedelta(days=validated_data['time_to_execute'])
        validated_data['is_active'] = True

        if validated_data['owner'].is_manager():
            validated_data['status'] = 'OE'
            validated_data['description'] = "Комментарий менеджера:" + validated_data['description']
        return super().create(validated_data)


    class Meta:
        model = cars_models.RepairRequest
        fields = [
            'id',
            'is_active',
            'type',
            'type_title',
            'owner',
            'owner_hidden',
            'engineer',
            'engineer_email',
            'car',
            'car_reg_number',
            'status',
            'status_display',
            'time_to_execute',
            'end_date',
            'description',
        ]
        read_only_fields = [
            'type',
            'owner',
            'engineer',
            'car',
            'end_date',
            'status_display',

        ]

        validators = [
            cars_custom_validators.CarOwnerOrManagerValidator,
            cars_custom_validators.IfUserIsManagerEngineerMustBeSpecifiedValidator,
        ]

        extra_kwargs = {
            # 'type': {'read_only': True},
            # 'owner': {'read_only': True},
            # 'engineer': {'read_only': True},
            # 'car': {'read_only': True},
            # 'end_date': {'read_only': True},
            'time_to_execute': {'write_only': True},
            'status': {'write_only': True},

        }


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор модели Car"""

    brand_name = serializers.CharField(label='Название марки:', write_only=True, validators=[cars_custom_validators.CarBrandExistValidator])
    brand = CarBrandSerializer(many=False, read_only=True)
    owner = serializers.HyperlinkedRelatedField(
            many=False,
            read_only=False,
            allow_null=True,
            required=False,
            view_name='user-detail',
            lookup_field='email',
            lookup_url_kwarg='email',
            queryset=account_models.UserModel.objects.filter(role='d'),
            label='Водитель'
        )
    docs = CarDocumentSerializer(many=True, read_only=True)
    reqs = RepairRequestSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['registration_number'] = validated_data['registration_number'].upper()
        validated_data['brand'] = cars_models.CarBrand.objects.get(title=validated_data.pop('brand_name'))
        return super().create(validated_data)

    class Meta:
        model = cars_models.Car
        fields = [
            'id',
            'registration_number',
            'brand',
            'brand_name',
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
            'last_inspection': {'validators': [cars_custom_validators.LastInspectionValidator]},
        }