import datetime
import os
import random
import string
from typing import Literal

from django.db import models

from apps.account import models as account_models

def return_file_directory(model_name: Literal['cars', 'users'], file_type: Literal['avatars', 'docs'],
                          primary_key: str, file: str) -> str:
    """Возвращает директорию, хранения аватарки машины или пользователя """
    file_name_and_extension = os.path.splitext(file)

    return f"{model_name}/{primary_key}/{file_type}/" \
           f"{file_name_and_extension[0]}_{datetime.datetime.today().date()}{file_name_and_extension[1]}"

def generator_activation_code():
    """Возвращает рандомную строку из 6 символов"""

    letters = string.ascii_lowercase
    length = 6

    while True:
        activation_code = ''.join(random.choice(letters) for i in range(length))
        if not account_models.UserModel.objects.filter(activation_code=activation_code):
            return activation_code