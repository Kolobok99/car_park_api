from django.db import models


class BaseModel(models.Model):
    """Базовая модель"""

    created_on = models.DateTimeField('Время создания ', auto_now_add=True)
    modified_on = models.DateTimeField('Время добавления', auto_now=True)

    class Meta:
        abstract = True

class Document(models.Model):
    """ Модель: Абстрактная модель документа """

    type = models.ForeignKey('DocType', verbose_name="Тип", on_delete=models.SET(None),
                             related_name='doc')
    start_date = models.DateField('Дата выдачи')
    end_date = models.DateField('Дата окончания')

    class Meta:
        abstract = True


class DocType(models.Model):
    """ Модель: Тип документа """

    KINDS = (
        ('m', 'Человек'),
        ('a', 'Машина'),
    )

    title = models.CharField('Наименования', max_length=255)
    car_or_user = models.CharField("Тип", max_length=1, choices=KINDS, default='a')

    def __str__(self):
        return f'{self.title} ({self.car_or_user})'

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'