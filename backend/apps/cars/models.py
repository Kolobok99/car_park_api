from django.db import models

from apps.account.models import UserModel
from apps.base.models import BaseModel, Document
from services.services import return_file_directory


class Car(BaseModel):
    """ Модель: Машина """

    def return_path_to_upload_avatar(self, *args):
        """Возвращает путь загрузки аватарки"""

        return return_file_directory('cars', 'avatar', self.registration_number)

    registration_number = models.CharField('Регистрационный номер', unique=True, max_length=6)
    brand = models.ForeignKey('CarBrand', verbose_name='Марка', on_delete=models.SET(1),
                              related_name='cars')

    region_code = models.PositiveSmallIntegerField('Код региона')
    owner = models.ForeignKey(UserModel, verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='my_cars', null=True, blank=True)

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

        return return_file_directory('cars', 'doc', self.owner.registration_number)

    owner = models.ForeignKey(Car, verbose_name="Владелец", on_delete=models.CASCADE,
                              related_name='my_docs')
    file = models.FileField('Копия', upload_to=return_path_to_upload_doc, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Документ машины'
        verbose_name_plural = 'Документы машины'


class RepairRequest(models.Model):
    """ Модель: Заявка на ремонт  """

    STATUS_CHOISES = (
        ('O', 'Ожидает рассмотрения менеджера'),
        ('OE', "Ожидает подтверждение механика"),
        ("REP", "Ремонтируется"),
        ('V', 'Выполнена'),
        ('P', 'Просрочена'),
        ('T', 'Отклонено')
    )

    URGENCY_CHOISES = (
        ('N', 'Не срочно'),
        ('U', 'Срочно'),
        ('S', 'Очень срочно'),
    )

    type = models.ForeignKey("TypeOfApplication", verbose_name='Тип заявки', on_delete=models.SET(None))
    owner = models.ForeignKey(UserModel, verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='repair_reqs', null=True)
    engineer = models.ForeignKey(UserModel, verbose_name='Механик', on_delete=models.SET(None),
                                 related_name='repair_reqs', null=True)
    car = models.ForeignKey(Car, verbose_name="Машина", on_delete=models.CASCADE, related_name='repair_reqs')

    time_to_execute = models.PositiveIntegerField('Время на выполнение',
                                                  default=0)
    end_date = models.DateField('Дата окончания', null=True, blank=True)

    is_active = models.BooleanField("Активность заявки", default=True)
    status = models.CharField('Статус', max_length=3, choices=STATUS_CHOISES, default='O')
    urgency = models.CharField('Cрочность', max_length=1, choices=URGENCY_CHOISES, default='N')

    description = models.TextField("Описание")
    manager_comment = models.TextField("Комментарий менеджера", null=True, blank=True)

    def __str__(self):
        if self.owner:
            return f"{self.pk}-{self.owner.last_name} + " \
                   f"{self.start_date} + {self.type} + {self.car.registration_number}"
        return f"{self.pk}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class TypeOfApplication(models.Model):
    """ Модель: Типы заявок  """

    title = models.CharField('Наименование', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'