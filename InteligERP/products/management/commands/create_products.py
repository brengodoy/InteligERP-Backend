from django.core.management.base import BaseCommand
from products.models import Object
from storage.models import Section, Warehouse

class Command(BaseCommand):
    help = 'Crea objetos de prueba'

    def handle(self, *args, **kwargs):

        #Remove if exists to-be-created object
        object = Object.objects.filter(product_id=1).first()
    
        if object:
            object.delete()

        #Remove if exists to-be-created section
        section = Section.objects.filter(id_section=1).first()
    
        if section:
            section.delete()

        #Remove if exists to-be-created warehouse
        warehouse = Warehouse.objects.filter(id_warehouse=1).first()
    
        if warehouse:
            warehouse.delete()

        # Create linked different class instancies
        warehouse = Warehouse.objects.create(
            id_warehouse=2, name='Zárate', address='Alvear 870', description='Depósito norte'
        )

        section = Section.objects.create(
            warehouse=warehouse, id_section=2, height=3000,
            length=250000, width=150000, max_weight=25000, description='Productos intermedios',
            available_storage=150
        )

        Object.objects.create(
            product_id=1, name='Alfajores x8 Terrabusi', height='80',
            length='400', width='150', weight='300',
            section=section, discontinued=False, stock=100
        )
        self.stdout.write(self.style.SUCCESS('Objetos, secciones y depósitos creados exitosamente'))