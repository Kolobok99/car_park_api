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

    class Meta:
        model = base_models.DocType
        fields = "__all__"
