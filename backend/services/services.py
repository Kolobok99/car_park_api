import datetime
import os
import random
import string
from typing import Literal

from django.db import models


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
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string