import datetime

import pytest

from apps.cars import models as cars_models
from apps.account import models as account_models
from apps.base import models as base_models


@pytest.fixture()
def manager():
    manager = account_models.UserModel.objects.create_user(
        email='manager@mail.com',
        password='manager_password',
        role='m',
        is_active=True,
    )

    return manager

@pytest.fixture()
def driver():
    driver = account_models.UserModel.objects.create_user(
        email='driver@mail.com',
        password='driver_password',
        role='d',
        is_active=True,
    )

    return driver


@pytest.fixture()
def doc_types():
    """Инициализирует два типа документов: СНИЛС (user) и тех. паспорт (car)"""


    doc_types_data = [
        {
            'title': 'СНИЛС',
            'car_or_user': 'c'
        },
        {
            'title': 'тех.паспорт',
            'car_or_user': 'm'
        }
    ]

    for type in doc_types_data:
        base_models.DocType.objects.create(**type)

    return base_models.DocType.objects.all()


@pytest.fixture()
def cards(driver, users):
    """Инициализирует два типа документов: СНИЛС (user) и тех. паспорт (car)"""

    cards_data = [
        {
            'limit': 1000,
            'balance': 500,
            'owner': account_models.UserModel.objects.last(),
            'number': '1234123412341234'
        },
        {
            'limit': 2000,
            'balance': 1000,
            'owner': None,
            'number': '7981798179817981'
        },
        {
            'limit': 3000,
            'balance': 1500,
            'owner': None,
            'number': '1111999911119999'
        },
        {
            'limit': 500,
            'balance': 10,
            'owner': driver,
            'number': '8888666688886666'
        },
    ]

    for card in cards_data:
        account_models.FuelCard.objects.create(**card)

    return  account_models.FuelCard.objects.all()


@pytest.fixture()
def brands():

    titles_brand = [
        'TOYOTA',
        'KIA',
        'BMW',
    ]
    for title in titles_brand:
        cars_models.CarBrand.objects.create(title=title)

    return cars_models.CarBrand.objects.all()

@pytest.fixture()
def cars(brands, manager, driver):
    """Инициализирует два типа документов: СНИЛС (user) и тех. паспорт (car)"""

    cars_data = [
        {
            'registration_number': 'A111AA',
            'brand': brands.get(title='TOYOTA'),
            'region_code': 86,
            'owner': None,
            'last_inspection': '2022-10-12'
        },
        {
            'registration_number': 'A222AA',
            'brand': brands.get(title='KIA'),
            'region_code': 111,
            'owner': driver,
            'last_inspection': '2022-10-12'
        },
        {
            'registration_number': 'A333AA',
            'brand': brands.get(title='BMW'),
            'region_code': 111,
            'owner': None,
            'last_inspection': '2022-10-12'
        },
        {
            'registration_number': 'A444AA',
            'brand': brands.get(title='KIA'),
            'region_code': 86,
            'owner': manager,
            'last_inspection': '2022-10-12'
        },
        {
            'registration_number': 'A555AA',
            'brand': brands.get(title='KIA'),
            'region_code': 111,
            'owner': None,
            'last_inspection': '2022-10-12'
        },
    ]

    for car in cars_data:
        cars_models.Car.objects.create(**car)

    return cars_models.Car.objects.all()

@pytest.fixture()
def users(manager, driver):

    for i in range(1, 5):
        u = account_models.UserModel.objects.create_user(
            email=f'driver_{i}@mail.com',
            password=f'driver_{i}@mail.com',
        )
        p = account_models.Profile.objects.create(
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            phone=f'7111222000{i}',
            user=u,
        )

    driver_profile = account_models.Profile.objects.create(
            first_name='Водитель',
            last_name='Водителев',
            patronymic='Водителевич',
            phone=f'71112221111',
            user=driver,
    )
    manager_profile = account_models.Profile.objects.create(
        first_name='Менеджер',
        last_name='Менеджеров',
        patronymic='Менеджерич',
        phone=f'79991234455',
        user=manager,
    )
    users = account_models.UserModel.objects.all()

    return users


@pytest.fixture()
def car_documents(cars,doc_types):
    for car in cars:
        cars_models.CarDocument.objects.create(
            start_date='2022-10-12',
            end_date='2024-10-12',
            type=doc_types.filter(car_or_user='c')[0],
            car=car
        )

    return cars_models.CarDocument.objects.all()


@pytest.fixture()
def user_documents(users, doc_types):
    for user in users:
        account_models.UserDocument.objects.create(
            start_date='2022-10-12',
            end_date='2024-10-12',
            type=doc_types.filter(car_or_user='m')[0],
            owner=user
        )

    return account_models.UserDocument.objects.all()

@pytest.fixture()
def repairs(cars, users, driver, repair_types):

    for i in range(3):
        cars_models.RepairRequest.objects.create(
            type=repair_types[i],
            owner=users[i],
            car=cars[i],
            time_to_execute=10,
            end_date=datetime.date.today() + datetime.timedelta(days=10),
            description='Тестовое описание'
        )

    driver_request = cars_models.RepairRequest.objects.create(
            type=repair_types[1],
            owner=users[1],
            car=cars.filter(owner=driver)[0],
            time_to_execute=10,
            end_date=datetime.date.today() + datetime.timedelta(days=10),
            description='Тестовая заявка водителя'
        )

    return cars_models.RepairRequest.objects.all()

@pytest.fixture()
def repair_types():
    """Инициализирует два типа документов: СНИЛС (user) и тех. паспорт (car)"""

    titles_repair_types = [
       'Плановый осмотр',
        'Замена колес',
        'Ремонт двигателя'
    ]

    for title in titles_repair_types:
        cars_models.RepairType.objects.create(title=title)

    return cars_models.RepairType.objects.all()


@pytest.fixture()
def nots(driver, manager, users, repairs):
    for r in repairs:
        account_models.Notification.objects.create(
            owner=r.owner,
            content=f"Тестовое уведомление",
            content_object=r
        )
    driver_not = account_models.Notification.objects.create(
            owner=driver,
            content=f"Тестовое уведомление водителя",
            content_object=repairs.filter(owner=driver)[0]
        )
    manager_not = account_models.Notification.objects.create(
            owner=manager,
            content=f"Тестовое уведомление менеджера",
            content_object=repairs.filter(owner=manager)[0]
        )

    return account_models.Notification.objects.all()