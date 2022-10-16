import re
from rest_framework import serializers


class CarOwnerOrManagerValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        request_user = serializer.context['request'].user
        if request_user is data.get('car').owner and request_user.is_manager():
            raise serializers.ValidationError("ошибка: выберите свой автомобиль!")


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
            raise serializers.ValidationError("Ошибка: введите номер в формате A123AA")