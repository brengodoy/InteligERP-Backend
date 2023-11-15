from django.http import JsonResponse
from .models import Object,Price
from .forms import CreateObjectForm,CreatePriceForm
import yaml,json
from stakeholders.models import Supplier
from django.db.models import Max
from storage.handlers import calculate_available_volume
from decimal import Decimal
from storage.models import Section

# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']
    
def create_object(request):
    if request.method == 'POST':
        form = CreateObjectForm(request.POST)
        if form.is_valid():
            object_instance = form.save(commit=False)
            section = object_instance.section
            volume = object_instance.height * object_instance.width * object_instance.length
            calculate_available_volume(section.id,True)
            if calculate_available_volume(section.id,True) < volume:
                return JsonResponse({'success': False, 'message': 'There is not enough space in the section for this object'})
            else:
                object_instance.save()
                calculate_available_volume(section.id,False)
                return JsonResponse({'success': True, 'message': 'Object created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'product_id' in error_dict:
                return JsonResponse({'success': False, 'message': 'The product_id entered already exist.'})
            elif 'section' in error_dict:
                return JsonResponse({'success': False, 'message': 'The section entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_object(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            object = Object.objects.get(id=id)
            return JsonResponse({'id':object.id,
                                 'product_id': object.product_id,
                                 'name': object.name,
                                 'height': object.height,
                                 'length': object.length,
                                 'width': object.width,
                                 'weight': object.weight,
                                 'section': object.section.id,
                                 'discontinued': object.discontinued})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_objects(request):
    if request.method == 'GET':
        objects = Object.objects.all()
        object_list = []
        for object in objects:
            object_list.append({'id':object.id,
                                 'product_id': object.product_id,
                                 'name': object.name,
                                 'height': object.height,
                                 'length': object.length,
                                 'width': object.width,
                                 'weight': object.weight,
                                 'section': object.section.id,
                                 'discontinued': object.discontinued})
        return JsonResponse({'objects': object_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_object(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            object = Object.objects.get(id=id)
            if 'section' in request.POST:
                try:
                    id_section = request.POST.get('section')
                    section = Section.objects.get(id=id_section)
                    object.section = section
                    object.save()
                except Supplier.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The section entered does not exist.'})
            if 'product_id' in request.POST:
                object.product_id = request.POST.get('product_id')
            if 'name' in request.POST:
                object.name = request.POST.get('name')
            if 'length' in request.POST:
                object.length = request.POST.get('length')
            if 'width' in request.POST:
                object.width = request.POST.get('width')
            if 'height' in request.POST:
                object.height = request.POST.get('height')
            if 'weight' in request.POST:
                object.weight = request.POST.get('weight')        
            if 'discontinued' in request.POST:
                object.discontinued = request.POST.get('discontinued')
            if any(key in request.POST for key in ['length', 'height', 'width']):
                volume = Decimal(object.length) * Decimal(object.width) * Decimal(object.height) * Decimal(object.stock)
                objects = Object.objects.filter(section=object.section.id).exclude(id=object.id)
                section = Section.objects.get(id=object.section.id)
                total_volume = 0
                for obj in objects:
                    total_volume = total_volume + (obj.height * obj.length * obj.width * obj.stock)
                available_storage = (section.height * section.width * section.length) - total_volume
                if available_storage < volume:
                    return JsonResponse({'success': True, 'message': 'There is not enough space in the section for this object'})
                else:
                    object.save()
                    calculate_available_volume(object.section.id,False)
            object.save()
            return JsonResponse({'success': True, 'message': 'Object updated successfully'})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
"""def delete_object(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            object = Object.objects.get(id=id)
            object.delete()
            return JsonResponse({'success': True, 'message': 'Object deleted successfully'})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})"""
    
def create_price(request):
    if request.method == 'POST':
        form = CreatePriceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Price created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'object' in error_dict:
                return JsonResponse({'success': False, 'message': 'The object entered does not exist.'})
            elif 'supplier' in error_dict:
                return JsonResponse({'success': False, 'message': 'The supplier entered does not exist.'})
            elif '__all__' in error_dict:
                return JsonResponse({'success': False, 'message': 'This datetime already exist for this object.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_price(request):
    if request.method == 'GET':
        id_object = request.GET.get('id_object')
        supplier_ids = request.GET.getlist('supplier_ids')
        try:
            object = Object.objects.get(id=id_object)
            if not supplier_ids:
                prices = Price.objects.filter(object=object).values('supplier').annotate(max_date=Max('date')).values('supplier', 'max_date')
            else:
                prices = Price.objects.filter(object=object, supplier_id__in=supplier_ids).values('supplier').annotate(max_date=Max('date')).values('supplier', 'max_date')

            price_data = []
            for price in prices:
                if not supplier_ids:
                    latest_price = Price.objects.filter(object=object, supplier_id=price['supplier'], date=price['max_date']).first()
                else:
                    latest_price = Price.objects.filter(object=object, supplier_id=price['supplier'], date=price['max_date']).first()

                price_data.append({
                    'name': object.name,
                    'price': latest_price.price,
                    'date': latest_price.date,
                    'currency': latest_price.currency,
                    'supplier': latest_price.supplier.id
                })
            return JsonResponse(price_data, safe=False)
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_price(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            price = Price.objects.get(id=id)
            price.delete()
            return JsonResponse({'success': True, 'message': 'Price deleted successfully'})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Price does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
