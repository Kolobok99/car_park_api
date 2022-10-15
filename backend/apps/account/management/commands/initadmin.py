from django.contrib.auth.models import User
from django.core.management import BaseCommand

from apps.account.models import UserModel


class Command(BaseCommand):
    help = 'Создает админа (root:root)'
    def handle(self, *args, **options):
        """Создает админа, если в БД нет ни одного user(is_superuser=True)"""

        if not UserModel.objects.filter(is_superuser=True):
            UserModel.objects.create_superuser(
                email='root@mail.com',
                password='root',
            )
            admin = UserModel.objects.get(is_superuser=True)
            admin.role = 'm'
            admin.save()
        try:
            UserModel.objects.create_user(
                email='driver@mail.com',
                password='12345'
            )
        except:
            pass
        self.stdout.write(self.style.SUCCESS("Админ создан!"))