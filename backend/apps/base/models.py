from django.db import models


class BaseModel(models.Model):
    """Базовая модель"""

    created_on = models.DateTimeField('Время создания ', auto_now_add=True)
    modified_on = models.DateTimeField('Время добавления', auto_now=True)

    class Meta:
        abstract = True
