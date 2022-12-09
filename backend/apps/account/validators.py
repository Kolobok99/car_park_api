import re
from pprint import pprint

from django.db.models import Q
from rest_framework import serializers

from apps.account import models as account_models
from services.services import get_value_by_instance_or_from_validate_data

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
            raise serializers.ValidationError(
                {'invalid_number_error': "Ошибка: номер карты состоит из 16 цифр"}
            )


class LimitAndBalanceValidator:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):
        balance = get_value_by_instance_or_from_validate_data(serializer.instance, data, 'balance')
        limit = get_value_by_instance_or_from_validate_data(serializer.instance, data, 'limit')
        if balance and balance > limit:
            raise serializers.ValidationError(
                {'balance_and_limit_error': "Ошибка: баланс не может превышать лимит"}
            )

class EngineerExistValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, engineer_email):
        car = account_models.UserModel.objects.filter(Q(email=engineer_email) and Q(role='e'))
        if not car:
            raise serializers.ValidationError(f"Ошибка: Инженер с email {engineer_email} не найдена")


def balance_only_updatable_validator(data: dict):
    data_keys = data.keys() # [limit, balance, owner]
    print(f'{data_keys=}')
    un_permitted_fields = ['limit', 'number', 'owner']
    result = list(set(data_keys) & set(un_permitted_fields))
    print(f"{result=}")
    if result:
        raise serializers.ValidationError(
            {'update_error': f"Ошибка: у вас нет прав для изменения {un_permitted_fields}"}
        )




class UserPasswordRepeatValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, data):
        if data.get('password') != data.get('repeat_password'):
            raise serializers.ValidationError(
                {'password_repeat_error': 'Ошибка: Пароли не совпадают!'}
            )


class ProfilePhoneValidator:

    def __init__(self, base):
        self.__call__(base)

    def __call__(self, phone):
        if not re.match(r'^7[0-9]{10}$', phone):
            raise serializers.ValidationError("ошибка: введите номер в формате 7XXXXXXXXXX")



class ManagerUserCanCreateOnlyManager:
    requires_context = True

    def __init__(self, base, serializer):
        self.__call__(base, serializer)

    def __call__(self, data, serializer):

        user = data.get('hidden_user')
        role = data.get('role')

        if not user.is_authenticated and role not in ['d', 'e']:
            raise serializers.ValidationError(
                {
                    'user_role_error': 'Ошибка: выберите одну из ролей (водитель/механик)'
                }
            )
        if user.is_authenticated:
            if not user.is_manager() and role not in ['d', 'e']:
                raise serializers.ValidationError(
                    {
                        'user_role_error': 'Ошибка: выберите одну из ролей (водитель/механик)'
                    }
                )
        # if role not in ['d', 'e']:
        #     if not user.is_authenticated:

