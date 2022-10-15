from rest_framework import serializers

from apps.account import models as account_models
from apps.cars import models as cars_models
from apps.base import models as base_models

from apps.api import validators as custom_validators
from services.services import generator_activation_code


class DocTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = base_models.DocType
        fields = "__all__"


class RepairRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = cars_models.RepairRequest
        fields = "__all__"
        validators = [
            custom_validators.CarOwnerOrManagerRepairRequestValidator,
        ]


class CarDocumentSerializer(serializers.ModelSerializer):

    type = serializers.PrimaryKeyRelatedField(label='тип', queryset=base_models.DocType.objects.filter(car_or_user='c'))

    class Meta:
        model = cars_models.CarDocument
        fields = "__all__"
        validators = [
            custom_validators.CarOwnerOrManagerDocumentValidator,
            custom_validators.DateValidator,
        ]


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор модели Car"""

    owner = serializers.HyperlinkedRelatedField(
            many=False,
            read_only=False,
            allow_null=True,
            view_name='user-detail',
            lookup_field='email',
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
        read_only_fields = ['docs', 'reqs', 'owner']
        extra_kwargs = {
            'registration_number': {'validators': [custom_validators.CarRegistrationNumberValidator]},
            'region_code': {'validators': [custom_validators.CarRegionCodeValidator]},
        }


class CarBrandSerializer(serializers.ModelSerializer):
    """Сериализатор модели CarBrand"""

    class Meta:
        model = cars_models.CarBrand
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = account_models.Profile
        fields = "__all__"
        extra_kwargs = {
            'first_name': {'validators': [custom_validators.ProfileFIOValidator]},
            'last_name': {'validators': [custom_validators.ProfileFIOValidator]},
            'patronymic': {'validators': [custom_validators.ProfileFIOValidator]},
            'phone': {'validators': [custom_validators.ProfilePhoneValidator]}
        }


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=['d', 'e'])
    profile = ProfileSerializer(read_only=False, many=False)
    repeat_password = serializers.CharField(label="Повтор пароля", write_only=True)
    reqs = RepairRequestSerializer(many=True, read_only=True)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('repeat_password')
        activation_code = generator_activation_code()
        user = account_models.UserModel.objects.create_user(activation_code=activation_code, **validated_data)
        profile = account_models.Profile.objects.create(user=user, **profile_data)
        return user

    class Meta:
        model = account_models.UserModel
        fields = [
            'email',
            'password',
            'repeat_password',
            'role',
            'profile',
            'docs'
                  ]
        validators = [custom_validators.UserPasswordRepeatValidator]
        extra_kwargs = {
            'password': {'write_only': True},
            'docs': {'read_only': True},
            'repeat_password': {'write_only': True},
        }


class UserDocumentSerializer(serializers.ModelSerializer):

    type = serializers.PrimaryKeyRelatedField(label='тип', queryset=base_models.DocType.objects.filter(car_or_user='m'))
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = account_models.UserDocument
        fields = "__all__"


class FuelCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.FuelCard
        fields = "__all__"

    extra_kwargs = {
        'number': {'validators': [custom_validators.FuelCardNumberValidator]},
    }
