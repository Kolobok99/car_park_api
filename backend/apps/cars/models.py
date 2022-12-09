from django.db import models

from apps.account.models import UserModel
from apps.base.models import BaseModel, Document
from services.services import return_file_directory


class Car(BaseModel):
    """ Модель: Машина """

    def return_path_to_upload_avatar(self, *args):
        """Возвращает путь загрузки аватарки"""

        return return_file_directory('cars', 'avatars', self.registration_number, self.image.name)

    registration_number = models.CharField('Регистрационный номер', unique=True, max_length=6)
    brand = models.ForeignKey('CarBrand', verbose_name='Марка', on_delete=models.SET(None),
                              related_name='cars', null=True)

    region_code = models.PositiveSmallIntegerField('Код региона')
    owner = models.ForeignKey(UserModel, verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='cars', null=True, blank=True)

    last_inspection = models.DateField("Последний осмотр", null=True, blank=True)

    image = models.ImageField('Фотография', null=True, blank=True, upload_to=return_path_to_upload_avatar)

    def __str__(self):
        return self.registration_number

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class CarBrand(BaseModel):
    """ Модель: Марка автомобиля """

    title = models.CharField(verbose_name='Марка', max_length=20, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class CarDocument(Document):
    """  Модель: Документ машины   """

    def return_path_to_upload_doc(self, *args):
        """Возвращает путь загрузки документа"""

        return return_file_directory('cars', 'docs', self.car.registration_number, self.file.name)

    car = models.ForeignKey(Car, verbose_name="Машина", on_delete=models.CASCADE,
                            related_name='docs')
    file = models.FileField('Копия', upload_to=return_path_to_upload_doc, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.car}"

    class Meta:
        verbose_name = 'Документ машины'
        verbose_name_plural = 'Документы машины'


class RepairRequest(BaseModel):
    """ Модель: Заявка на ремонт  """

    STATUS_CHOISES = (
        ('O', 'Ожидает рассмотрения менеджера'),
        ('OE', "Ожидает подтверждение механика"),
        ("REP", "Ремонтируется"),
        ('V', 'Выполнена'),
        ('P', 'Просрочена'),
        ('T', 'Отклонено')
    )


    type = models.ForeignKey("RepairType", verbose_name='Тип заявки', null=True, on_delete=models.SET(None))
    owner = models.ForeignKey(UserModel, verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='reqs', null=True)
    engineer = models.ForeignKey(UserModel, verbose_name='Механик', on_delete=models.SET(None),
                                 related_name='repair_reqs', null=True, blank=True)
    car = models.ForeignKey(Car, verbose_name="Машина", on_delete=models.CASCADE, related_name='reqs')

    time_to_execute = models.PositiveIntegerField('Время на выполнение')
    end_date = models.DateField('Дата окончания', null=True, blank=True)

    is_active = models.BooleanField("Активность заявки", default=True)
    status = models.CharField('Статус', max_length=3, choices=STATUS_CHOISES, default='O')

    description = models.TextField("Описание")

    def __str__(self):
        if self.owner:
            return f"{self.pk}-{self.owner.profile.last_name} + " \
                   f"{self.created_on} + {self.type} + {self.car.registration_number}"
        return f"{self.pk}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class RepairType(models.Model):
    """ Модель: Типы заявок  """

    title = models.CharField('Наименование', max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'
