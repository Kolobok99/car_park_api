import datetime
from typing import Literal


def return_avatar_directory(model_name: Literal['cars', 'users'], uniq_id):
    """Возвращает директорию, хранения аватарки машины или пользователя """

    return f"{model_name}/{uniq_id}/avatars/avatar_{datetime.datetime.today()}.webp"