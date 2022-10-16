from django.utils import timezone
from rest_framework import serializers


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
