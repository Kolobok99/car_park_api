import re
from rest_framework import serializers


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


class FuelCardNumberValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, number):
        if not re.match(r'^\d{16}$', number):
            raise serializers.ValidationError("Ошибка: номер карты состоит из 16 цифр")


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
        if not re.match(r'^7[0-9]{10}$', phone):
            raise serializers.ValidationError("ошибка: введите номер в формате 7XXXXXXXXXX")


