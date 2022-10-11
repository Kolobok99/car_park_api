# Generated by Django 4.1.2 on 2022-10-11 15:44

import apps.account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Время создания ')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Время добавления')),
                ('email', models.EmailField(error_messages={'invalid': 'Некорректный email', 'unique': 'Пользователь с таким email уже существует.'}, max_length=254, unique=True, verbose_name='Почта')),
                ('password', models.CharField(max_length=128, verbose_name='Пароль')),
                ('role', models.CharField(choices=[('a', 'admin'), ('m', 'manager'), ('d', 'driver'), ('e', 'engineer')], default='d', max_length=1, verbose_name='Роль')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активирован?')),
                ('activation_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Код активации аккаунта')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=20, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Номер телефона')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.account.models.Profile.path_to_upload_image, verbose_name='Аватарка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
