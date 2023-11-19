from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from storage.models import Warehouse

class Command(BaseCommand):
    help = 'Crea depósitos de prueba'

    def handle(self, *args, **kwargs):
        try:
            warehouse = Warehouse.objects.get(id_warehouse=1)
            warehouse.delete()
        except ObjectDoesNotExist:
            self.stdout.write(self.style.HTTP_INFO('Warehouse id_warehouse=1 no existía previamente'))
        Warehouse.objects.create(
            id_warehouse=1, name='Rosario', address='Zeballos 1523', description='Casa central'
        )
        self.stdout.write(self.style.SUCCESS('Warehouses creados exitosamente'))