from rest_framework import serializers

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import validators as base_custom_validators
from apps.account import validators as account_custom_validators
from apps.cars import validators as cars_custom_validators


from apps.base import serializers as base_serializers
from apps.cars import serializers as cars_serializers

from services import services
from apps.polls import tasks


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = account_models.Profile
        fields = [
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'image',
        ]
        extra_kwargs = {
            'first_name': {'validators': [account_custom_validators.ProfileFIOValidator]},
            'last_name': {'validators': [account_custom_validators.ProfileFIOValidator]},
            'patronymic': {'validators': [account_custom_validators.ProfileFIOValidator]},
            'phone': {'validators': [account_custom_validators.ProfilePhoneValidator]}
        }


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=['d', 'e'])
    profile = ProfileSerializer(read_only=False, many=False)
    repeat_password = serializers.CharField(label="Повтор пароля", write_only=True)
    reqs = cars_serializers.RepairRequestSerializer(many=True, read_only=True)

    def create(self, validated_data):
        activation_code = services.generator_activation_code()
        profile_data = validated_data.pop('profile')
        validated_data.pop('repeat_password')
        user = account_models.UserModel.objects.create_user(activation_code=activation_code, **validated_data)
        profile = account_models.Profile.objects.create(user=user, **profile_data)
        tasks.send_activation_code.delay(driver_email=user.email, activation_code=activation_code)
        return user

    class Meta:
        model = account_models.UserModel
        fields = [
            'email',
            'password',
            'repeat_password',
            'role',
            'profile',
            'docs',
            'reqs'
                  ]
        validators = [account_custom_validators.UserPasswordRepeatValidator]
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
        'number': {'validators': [account_custom_validators.FuelCardNumberValidator]},
    }


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        modul=account_models.Notification
        fields = "__all__"
