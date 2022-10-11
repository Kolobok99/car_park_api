import datetime

from PIL import Image

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.base.models import BaseModel


class UserManager(BaseUserManager):
    """
        Менеджер: модели MyUser
    """

    def create_user(self, email, password, **extra_fields):
        """ Создание user'а """
        if not email:
            raise ValueError("Укажите Email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return UserModel

    def create_superuser(self, email, password, **extra_fields):
        """Создание root'а """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Root должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Root должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class UserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ Модель: Пользователь """

    # Типы user'ов
    KINDES = (
        ('a', 'admin'),
        ('m', 'manager'),
        ('d', 'driver'),
        ('e', 'engineer'),
    )

    email = models.EmailField('Почта', unique=True,
                              error_messages={
                                  'unique': 'Пользователь с таким email уже существует.',
                                  'invalid': 'Некорректный email'
                              })
    password = models.CharField("Пароль", max_length=128)
    role = models.CharField('Роль', max_length=1, choices=KINDES, default='d')
    is_active = models.BooleanField("Активирован?", default=False)
    activation_code = models.CharField("Код активации аккаунта", max_length=6, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # заглушка для избежания ошибок переопределения AbstractBaseUser
    last_login = None

    def update_last_login(sender, user, **kwargs):
        pass

    def is_manager(self):
        return True if self.role == 'm' else False

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    """Модель: Профиль пользователя"""

    def path_to_upload_image(self, *args):
        """Возвращает путь загрузки фотографии"""

        path = f"users/{self.user.email}/avatars/user_avatar_{datetime.datetime.today()}.webp"
        return path

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user')
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20, )
    patronymic = models.CharField('Отчество', max_length=20)
    phone = models.CharField('Номер телефона', max_length=11, unique=True)

    image = models.ImageField('Аватарка', null=True, blank=True, upload_to=path_to_upload_image)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'