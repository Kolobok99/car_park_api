from rest_framework import serializers

from apps.base import models as base_models
from apps.account import models as account_models
from apps.cars import models as cars_models

from apps.base import validators as base_custom_validators
from apps.account import validators as account_custom_validators
from apps.cars import validators as cars_custom_validators


from apps.cars import serializers as cars_serializers


from services import services
from apps.polls import tasks


class DocTypeSerializer(serializers.ModelSerializer):

    car_or_user_display = serializers.ChoiceField(choices=[('c', 'Машина'), ('m', 'Водитель')], source='get_car_or_user_display', read_only=True)

    class Meta:
        model = base_models.DocType
        fields = [
            'id',
            'created_on',
            'modified_on',
            'title',
            'car_or_user',
            'car_or_user_display'
        ]
        extra_kwargs = {
            'car_or_user': {'write_only': True}
        }
