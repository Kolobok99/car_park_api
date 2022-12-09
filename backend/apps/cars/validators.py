import re

from django.utils import timezone
from rest_framework import serializers
from apps.cars import models as cars_models

class CarOwnerOrManagerValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        print("START OWNER VALIDATOR")
        request_user = serializer.context['request'].user
        car = cars_models.Car.objects.get(registration_number=data.get('car_reg_number').upper())
        print(request_user)
        print(car.owner)
        if request_user != car.owner:
            raise serializers.ValidationError("ошибка: выберите свой автомобиль!")


class IfUserIsManagerEngineerMustBeSpecifiedValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        request_user = serializer.context['request'].user
        if request_user.is_manager() and not data.get('engineer_email', None):
            raise serializers.ValidationError(
                {'engineer_email_specified_error': "Ошибка: укажите email механика"}
            )
        elif not request_user.is_manager() and data.get('engineer_email'):
            raise serializers.ValidationError(
                {'engineer_email_forbidden_error': "Ошибка: механика может указать только менеджер!"}
            )


class CarRegionCodeValidator:
    """Валидатор RegionCode"""

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, region_code):
        if region_code > 200:
            raise serializers.ValidationError("Ошибка: 0 < region_code < 200")


class CarRegistrationNumberValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, registration_number):
        if not re.match(r'^[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{2}$', registration_number):
            raise serializers.ValidationError(
                {'registration_number_error_key': "Ошибка: введите номер в формате A123AA"}
            )

class CarBrandExistValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, brand_name):
        brand = cars_models.CarBrand.objects.filter(title=brand_name).first()
        print(f"{brand=}")
        if not brand:
            raise serializers.ValidationError({
                'brand_not_exist_error': "Ошибка: марка {brand_name} не найдена"
            })


class CarExistValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, car_reg_number):
        print("ASDASDASDASD")
        car = cars_models.Car.objects.filter(registration_number__iexact=car_reg_number).first()
        if not car:
            raise serializers.ValidationError(f"Ошибка: машина {car_reg_number} не найдена")


class TypeOfRepairExistValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, type_title):
        car = cars_models.RepairType.objects.filter(title=type_title)
        if not car:
            raise serializers.ValidationError(f"Ошибка: Тип заяки {type_title} не найдена")

class LastInspectionValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, last_inspection):
        errors = {}
        current_date = timezone.now().date()

        if last_inspection > current_date:
            errors['last_inspection_date_error'] = "Ошибка: дата последнего осмотра больше текущей"

        if errors:
            raise serializers.ValidationError(errors)


def image_and_last_inspection_only_updatable_validator(data: dict):
    data_keys = data.keys()
    un_permitted_fields = ['registration_number', 'brand',
                           'region_code', ' owner']
    result = list(set(data_keys) & set(un_permitted_fields))
    print(f"{result=}")
    if result:
        raise serializers.ValidationError(
            {'update_error': f"Ошибка: у вас нет прав для изменения {un_permitted_fields}"}
        )