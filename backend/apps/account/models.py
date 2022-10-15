from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.base.models import BaseModel, Document
from services.services import return_file_directory


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
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание root'а """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'a')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Root должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Root должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class UserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ Модель: Пользователь """

    # Типы user'ов
    KINDS = (
        ('a', 'admin'),
        ('m', 'manager'),
        ('d', 'driver'),
        ('e', 'engineer'),
    )

    email = models.EmailField('Почта', primary_key=True,
                              error_messages={
                                  'unique': 'Пользователь с таким email уже существует.',
                                  'invalid': 'Некорректный email'
                              })
    password = models.CharField("Пароль", max_length=128)
    role = models.CharField('Роль', max_length=1, choices=KINDS, default='d')
    is_active = models.BooleanField("Активирован?", default=False, editable=False)
    activation_code = models.CharField("Код активации аккаунта", max_length=6, editable=False)
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
        return True if self.is_authenticated and self.role == 'm' else False

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    """Модель: Профиль пользователя"""

    def return_path_to_upload_avatar(self, *args):
        """Возвращает путь загрузки аватарки"""

        return return_file_directory('users', 'avatars', self.user.email, self.image.name)


    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20, )
    patronymic = models.CharField('Отчество', max_length=20)
    phone = models.CharField('Номер телефона', max_length=11, unique=True)

    image = models.ImageField('Аватарка', null=True, blank=True, upload_to=return_path_to_upload_avatar)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UserDocument(Document):
    """ Модель: Документы пользователя  """

    def return_path_to_upload_doc(self, *args):
        """Возвращает путь загрузки документа"""

        return return_file_directory('users', 'doc', self.owner.email)

    owner = models.ForeignKey(UserModel, verbose_name="Владелец", on_delete=models.CASCADE,
                              related_name='docs')
    file = models.FileField('Копия', upload_to=return_path_to_upload_doc, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Документ водителя'
        verbose_name_plural = 'Документы водителя'


class FuelCard(BaseModel):
    """ Модель: Топливная карта"""

    limit = models.PositiveIntegerField('Лимит')
    number = models.CharField('Номер', primary_key=True, max_length=16)

    owner = models.OneToOneField(UserModel, verbose_name='Владелец', on_delete=models.SET(None),
                                 related_name='card', blank=True, null=True)

    balance = models.PositiveIntegerField('Остаток', null=True, blank=True)

    def __str__(self):
        # 1234-5678-1234-5678
        return f"{self.number[0:4]}-{self.number[4:8]}-{self.number[8:12]}-{self.number[12:16]}"

    class Meta:
        verbose_name = 'Топливная карта'
        verbose_name_plural = 'Топливные карты'



class WhiteListEmail(models.Model):
    """  Модель: email разрешенный для регистрации """

    email = models.EmailField('Email', unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'White List of Emil'
        verbose_name_plural = 'White List of Emil'