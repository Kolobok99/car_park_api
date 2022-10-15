import re
from pprint import pprint
from django.utils import timezone
from rest_framework import serializers


class FuelCardNumberValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, number):
        if not re.match(r'^\d{16}$', number):
            raise serializers.ValidationError("Ошибка: номер карты состоит из 16 цифр")


class CarRegistrationNumberValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, registration_number):
        # [a - zA - Z]{1}[0 - 9]{3}[a - zA - Z]{2}
        if not re.match(r'^[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{2}$', registration_number):
            raise serializers.ValidationError("Ошибка: введите номер в формате A123AA")


class CarRegionCodeValidator:
    """Валидатор RegionCode"""

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, region_code):
        if region_code > 200:
            raise serializers.ValidationError("Ошибка: 0 < region_code < 200")

class ProfileFIOValidator:
    """Валидатор FIO (first_name, last_name, patronymic)"""

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, fio_data):
        errors = {}
        if not fio_data[0].isupper():
            errors['first_letter_error'] = f'Ошибка: первая буква должна быть заглавной!'
        if re.search(r'[a-zA-Z]|\d', fio_data) or not fio_data.isalpha():
            errors['latin_error'] = f'Ошибка: ФИО состоит только из латиницы'


        if errors:
            raise serializers.ValidationError(errors)


class UserPasswordRepeatValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, data):
        if data.get('password') != data.get('repeat_password'):
            raise serializers.ValidationError('Ошибка: Пароли не совпадают!')

class ProfilePhoneValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, phone):
        print("YES!")
        if not re.match(r'^7[0-9]{10}$', phone):
            raise serializers.ValidationError("ошибка: введите номер в формате 7XXXXXXXXXX")


class CarOwnerOrManagerDocumentValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        request_user = serializer.context['request'].user
        print(data.get('car').owner)
        if not (request_user is data.get('car').owner or request_user.is_manager()):
            raise serializers.ValidationError("ошибка: выберите свой автомобиль!")


class CarOwnerOrManagerRepairRequestValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        print(f"{data.get('car').owner=}")
        print(f"{serializer.context['request'].user.is_manager()=}")
        request_user = serializer.context['request'].user
        if request_user is data.get('car').owner and request_user.is_manager():
            raise serializers.ValidationError("ошибка: выберите свой автомобиль!")


class DateValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, data):
        errors = {}
        current_date = timezone.now().date()

        if data.get('start_date') > data.get('end_date'):
            errors['end_date_error'] = "Ошибка: start_date < end_date"
        if data.get('start_date') > current_date:
            errors['end_date_error'] = "Ошибка: start_date > current_date"

        if errors:
            raise serializers.ValidationError(errors)