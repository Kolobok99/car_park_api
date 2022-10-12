from django.db import models

from services.services import return_avatar_directory


class Car(models.Model):
    """ Модель: машина """

    def return_path_to_upload_image(self, *args):
        """Возвращает путь загрузки фотографии"""

        return return_avatar_directory('cars', self.registration_number )

    registration_number = models.CharField('Регистрационный номер', unique=True, max_length=6)
    brand = models.ForeignKey('CarBrand', verbose_name='Марка', on_delete=models.SET(1),
                              related_name='cars')

    region_code = models.PositiveSmallIntegerField('Код региона')
    owner = models.ForeignKey('MyUser', verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='my_cars', null=True, blank=True)

    last_inspection = models.DateField("Последний осмотр", null=True, blank=True)

    image = models.ImageField('Фотография', null=True, blank=True, upload_to=path_to_upload_image)

    def __str__(self):
        return self.registration_number

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
