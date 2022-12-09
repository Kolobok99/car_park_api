import datetime
import os
import random
import re
import string
from typing import Literal, OrderedDict, Union

from django.core.files import File
from django.conf import settings
from django.db import models
from django.db.models import Model
from django.http import QueryDict

from apps.account import models as account_models

def return_file_directory(model_name: Literal['cars', 'users'], file_type: Literal['avatars', 'docs'],
                          primary_key: str, file: str) -> str:
    """Возвращает директорию, хранения аватарки машины или пользователя """
    file_name_and_extension = os.path.splitext(file)

    return f"{model_name}/{primary_key}/{file_type}/" \
           f"{file_type[0:-1]}_{datetime.datetime.today().date()}{file_name_and_extension[1]}"


def generator_activation_code():
    """Возвращает рандомную строку из 6 символов"""

    letters = string.ascii_lowercase
    length = 6

    while True:
        activation_code = ''.join(random.choice(letters) for i in range(length))
        if not account_models.UserModel.objects.filter(activation_code=activation_code):
            return activation_code


def get_value_by_instance_or_from_validate_data(instance: Model, data: OrderedDict, key: Union[str, QueryDict]):
    """Возвращает значение поля из data или instance по key"""

    try:
        value = data[key]
    except KeyError:
        value = getattr(instance, key, None)

    return value


def change_file_directory(instance, validated_data):

    os.renames(
        f'{settings.MEDIA_ROOT}/users/{instance.email}',
        f'{settings.MEDIA_ROOT}/users/{validated_data.get("email")}'
    )
    # Если у профиля есть аватарка
    if instance.profile.image:
        image_name = os.path.basename(instance.profile.image.name)
        avatar_path = f'users/{validated_data.get("email")}/avatars/{image_name}'

        instance.profile.image = avatar_path
        instance.profile.save()


def return_url_without_schema_address(url):

    return re.search(r"//[^\/]+(.*)", url).group(1)