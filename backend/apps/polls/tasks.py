import datetime

from django.core.mail import send_mail
from django.db.models import Q

from apps.cars import models as cars_models
from apps.account import models as account_models
from conf.celery import app


@app.task
def check_last_inspection():
    """
    Проверяет дату последнего ТО авто.
    Если срок действия осмотра истекает, создает новую заявку на ТО
    """
    today = datetime.date.today()

    pto_req = cars_models.TypeOfApplication.objects.get_or_create(title='ПТО')
    cars_without_pto_reqs = cars_models.Car.objects.filter(reqs__type__exact=pto_req)

    for car in cars_without_pto_reqs:
        time_delta = today - car.last_inspection
        if time_delta <= datetime.timedelta(days=30):
            cars_models.RepairRequest.objects.create(
                car=car,
                type=pto_req,
                owner=None,
                description='Заявка на плановый осмотр'
            )


@app.task
def check_car_docs_date():
    """
    Проверяет срок действия документов авто.
    Если срок действия истекает, создает уведомление владельцу авто
    """
    time_delta = datetime.timedelta(days=10)
    today = datetime.date.today()
    car_docs_with_expiration_date = cars_models.CarDocument.objects.filter(
       end_date__lte=today-time_delta
    )

    for car_doc in car_docs_with_expiration_date:
        account_models.Notification.objects.get_or_create(
            recipient=car_doc.owner.owner,
            content=f"Срок действия документа на машину {car_doc.car.registration_number}"
                    f" истекает через {time_delta}",
            content_object=car_doc
        )

@app.task
def check_user_docs_date():
    """
    Проверяет срок действия документов водителя.
    Если срок действия истекает, создает уведомление водитлею
    """

    time_delta = datetime.timedelta(days=10)
    today = datetime.date.today()
    user_docs_with_expiration_date = account_models.UserDocument.objects.filter(
        end_date__lte=today - time_delta
    )

    for user_doc in user_docs_with_expiration_date:
        account_models.Notification.objects.get_or_create(
            recipient=user_doc.owner,
            content=f"Срок действия документа {user_doc}"
                    f" истекает через {time_delta}",
            content_object=user_doc
        )


@app.task
def send_activation_code(driver_email, activation_code):
    """Отправляет код активации аккаунта"""
    send_mail(
        'Подтверждение регистрации',
        f'ВАШ КОД: {activation_code}',
        'zolotavin011@mail.ru',
        [driver_email],
        fail_silently=False
    )


@app.task
def delete_empty_card():
    """Удаляет карты с 0 балансом"""
    account_models.FuelCard.objects.filter(balance=0).delete()


@app.task
def create_note_about_ending_cards():
    """
    Создает уведолмение менеджеру о том,
    что заканчиваются свободные карты
    """
    cards = account_models.FuelCard.objects.filter(owner__isnull=True)
    if len(cards) < 2:
        account_models.Notification.objects.create(
            recipient=account_models.UserModel.objects.get(role='m'),
            content=f"Заканчиваются карты, осталось {len(cards)} штуки",
            content_object=account_models.UserModel.objects.get(role='m')
        )

@app.task
def checking_timing_app():
    """Создает уведомление о просроченности заявки"""

    today = datetime.date.today()
    active_reqs_with_expiration_date = cars_models.RepairRequest.objects.filter(
        Q(is_active=True)
        and Q(end_date__gt=today)
        and Q(owner__activation_code__isnull=False)
    )
    for req in active_reqs_with_expiration_date:
        # Уведомление механику
        account_models.Notification.objects.create(
                recipient=req.engineer,
                content=f"Вы просрочили выполнение заявки {app.pk}",
                content_object=app
            )
        # Уведомление менеджеру
        account_models.Notification.objects.create(
                recipient=account_models.UserModel.objects.get(role='m'),
                content=f"Механик ({app.engineer}) просрочил выполнение заявки {app.pk}",
                content_object=app
            )