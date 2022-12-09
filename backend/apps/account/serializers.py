import os

from django.conf import settings
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from rest_framework import validators

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.account import validators as account_custom_validators

from apps.cars import serializers as cars_serializers

from services import services
from apps.polls import tasks


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = account_models.Profile
        fields = [
            'id',
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
            'phone': {'validators': [ validators.UniqueValidator(queryset=model.objects.all()),
                                      account_custom_validators.ProfilePhoneValidator,
                                     ]}
        }


class UserSerializer(serializers.ModelSerializer):

    role_display = serializers.ChoiceField(choices=account_models.UserModel.CHOICES, source='get_role_display', read_only=True)
    repeat_password = serializers.CharField(label="Повтор пароля", write_only=True)

    reqs = cars_serializers.RepairRequestSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=False, many=False)

    hidden_user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)

    def create(self, validated_data):
        if not account_models.WhiteListEmail.objects.filter(email=validated_data.get('email')).first():
            raise serializers.ValidationError(
                {"email_whitelist_error": 'Ошибка: ваш еmail не указан в списке допустимых'}
            )
        validated_data.pop('hidden_user')
        activation_code = services.generator_activation_code()
        profile_data = validated_data.pop('profile')
        validated_data.pop('repeat_password')
        user = account_models.UserModel.objects.create_user(activation_code=activation_code, **validated_data)
        profile = account_models.Profile.objects.create(user=user, **profile_data)
        tasks.send_activation_code.delay(driver_email=user.email, activation_code=activation_code)

        return user

    def update(self, instance: account_models.UserModel, validated_data):
        profile_data = validated_data.pop('profile', None)
        validated_data.pop('repeat_password', None)
        password = validated_data.pop('password', None)

        if instance.email != validated_data.get('email'):
            services.change_file_directory(instance, validated_data)

        instance = super(UserSerializer, self).update(instance, validated_data)
        if profile_data:
            image = profile_data.pop('image', None)
            account_models.Profile.objects.filter(user=instance).update(**profile_data)
            profile = account_models.Profile.objects.get(user=instance)
            if image:
                profile.image = image
                profile.save()

        if password:
            instance.set_password(password)
            instance.save()

        return account_models.UserModel.objects.get(email=instance.email)


    class Meta:
        model = account_models.UserModel
        fields = [
            'hidden_user',
            'id',
            'email',
            'password',
            'repeat_password',
            'role',
            'role_display',
            'profile',
            'docs',
            'reqs'
                  ]
        lookup_field = "email"
        validators = [
            account_custom_validators.UserPasswordRepeatValidator,
            account_custom_validators.ManagerUserCanCreateOnlyManager,
                      ]
        extra_kwargs = {
            'password': {'write_only': True},
            'docs': {'read_only': True},
            'reqs': {'read_only': True},
            'role': {'write_only': True,
                     'choices': account_models.UserModel.CHOICES,
                     },
            'repeat_password': {'write_only': True},
        }


class UserDocumentSerializer(serializers.ModelSerializer):

    type = serializers.PrimaryKeyRelatedField(label='тип', queryset=base_models.DocType.objects.filter(car_or_user='m'))
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)

    # def create(self, validated_data):
    #     validated_data['owner'] = validated_data.pop('owner_hidden')
    #     return super(UserDocumentSerializer, self).create(validated_data)

    class Meta:
        model = account_models.UserDocument
        fields = [f.name for f in account_models.UserDocument._meta.get_fields()]


class FuelCardSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['balance'] = validated_data['limit']
        return super(FuelCardSerializer, self).create(validated_data)

    class Meta:
        model = account_models.FuelCard
        fields = "__all__"
        validators = [
            account_custom_validators.LimitAndBalanceValidator
        ]
        extra_kwargs = {
            'number': {'validators': [account_custom_validators.FuelCardNumberValidator]},

        }



class NotificationSerializer(serializers.ModelSerializer):

    owner_email = serializers.EmailField(label='Email получателя', write_only=True)

    content_object = GenericRelatedField({
        account_models.FuelCard: serializers.HyperlinkedRelatedField(
            queryset=account_models.FuelCard.objects.all(),
            view_name='card-detail',
            many=False,
            lookup_field='number'
        ),
        account_models.UserModel: serializers.HyperlinkedRelatedField(
            queryset=account_models.UserModel.objects.all(),
            view_name='user-detail',
            many=False,
            lookup_field='email'
        ),
        account_models.UserDocument: serializers.HyperlinkedRelatedField(
            queryset=account_models.UserDocument.objects.all(),
            view_name='user_doc-detail',
            many=False,
            lookup_field='pk'
        ),
        cars_models.Car: serializers.HyperlinkedRelatedField(
            queryset=cars_models.Car.objects.all(),
            view_name='car-detail',
            many=False,
            lookup_field='registration_number'
        ),
        cars_models.RepairRequest: serializers.HyperlinkedRelatedField(
            queryset=cars_models.RepairRequest.objects.all(),
            view_name='repair-detail',
            many=False,
            lookup_field='pk'
        ),
        cars_models.CarDocument: serializers.HyperlinkedRelatedField(
            queryset=cars_models.CarDocument.objects.all(),
            view_name='car_doc-detail',
            many=False,
            lookup_field='pk'
        )
    })

    def create(self, validated_data):
        validated_data['owner'] = account_models.UserModel.objects.get(email=validated_data.pop('owner_email'))
        return super(NotificationSerializer, self).create(validated_data)
    class Meta:
        model = account_models.Notification

        fields = [
            'id',
            'owner',
            'owner_email',
            'content',
            'content_object',
        ]
        extra_kwargs = {
            'is_active': {'read_only': True},
            'owner': {'read_only': True},

        }

