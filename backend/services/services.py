import datetime
from typing import Literal

from django.db import models


def return_file_directory(model_name: Literal['cars', 'users'], file_type: Literal['avatar', 'doc'], uniq_id: models.CharField) -> str:
    """Возвращает директорию, хранения аватарки машины или пользователя """

    return f"{model_name}/{uniq_id}/{file_type}/{file_type}_{datetime.datetime.today()}.webp"