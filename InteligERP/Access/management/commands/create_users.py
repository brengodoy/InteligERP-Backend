from django.core.management.base import BaseCommand
from access.models import User

class Command(BaseCommand):
    help = 'Crea usuarios de prueba'

    def handle(self, *args, **kwargs):
        User.objects.create_user(
            'tinchoabc', 'mb@mail.com', 'tincho123',
            is_superuser=1, first_name='Martin', last_name='Ballestero'
        )
        self.stdout.write(self.style.SUCCESS('Usuarios creados exitosamente'))