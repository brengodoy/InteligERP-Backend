from django.http import JsonResponse
from storage.models import Warehouse,Section
from storage.forms import CreateWarehouseForm,CreateSectionForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml,json

# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']

def create_warehouse(request):
    if request.method == 'POST':
        form = CreateWarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Warehouse created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_warehouse(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            warehouse = Warehouse.objects.get(id=id)
            if 'id_warehouse' in request.POST:
                warehouse.id_warehouse = request.POST.get('id_warehouse')
            if 'name' in request.POST:
                warehouse.name = request.POST.get('name')
            if 'address' in request.POST:
                warehouse.address = request.POST.get('address')
            if 'description' in request.POST:
                warehouse.description = request.POST.get('description')
            warehouse.save()
            return JsonResponse({'success': True, 'message': 'Warehouse updated successfully'})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_warehouse(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            warehouse = Warehouse.objects.get(id=id)
            return JsonResponse({'id':warehouse.id,
                                 'name': warehouse.name,
                                 'address': warehouse.address,
                                 'description': warehouse.description})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_all_warehouses(request):
    if request.method == 'GET':
        warehouses = Warehouse.objects.all()
        warehouse_list = []
        for warehouse in warehouses:
            warehouse_list.append({'id':warehouse.id,
                                   'name': warehouse.name,
                                   'address': warehouse.address,
                                   'description': warehouse.description})
        return JsonResponse({'warehouses': warehouse_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_warehouse(request):
    if request.method == 'POST':
        id_warehouse = request.POST.get('id_warehouse')
        try:
            warehouse = Warehouse.objects.get(id_warehouse=id_warehouse)
            warehouse.delete()
            return JsonResponse({'success': True, 'message': 'Warehouse deleted successfully'})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def create_section(request):
    if request.method == 'POST':
        form = CreateSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Section created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'warehouse' in error_dict:
                return JsonResponse({'success': False, 'message': 'The warehouse entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_section(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            section = Section.objects.get(id=id)
            return JsonResponse({'id':section.id,
                                 'warehouse': section.warehouse.id,
                                 'id_section': section.id_section,
                                 'height': section.height,
                                 'length': section.length,
                                 'width': section.width,
                                 'max_weight': section.max_weight,
                                 'description': section.description})
        except Section.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Section does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_sections(request):
    if request.method == 'GET':
        sections = Section.objects.all()
        section_list = []
        for section in sections:
            section_list.append({'id':section.id,
                                 'warehouse': section.warehouse.id,
                                 'id_section': section.id_section,
                                 'height': section.height,
                                 'length': section.length,
                                 'width': section.width,
                                 'max_weight': section.max_weight,
                                 'description': section.description})
        return JsonResponse({'sections': section_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_section(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            section = Section.objects.get(id=id)
            if 'warehouse' in request.POST:
                try:
                    id_warehouse = request.POST.get('warehouse')
                    warehouse = Warehouse.objects.get(id=id_warehouse)
                    section.warehouse = warehouse
                except Warehouse.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The warehouse entered does not exist.'})
            if 'id_section' in request.POST:
                section.id_section = request.POST.get('id_section')
            if 'height' in request.POST:
                section.height = request.POST.get('height')
            if 'length' in request.POST:
                section.length = request.POST.get('length')
            if 'width' in request.POST:
                section.width = request.POST.get('width')
            if 'max_weight' in request.POST:
                section.max_weight = request.POST.get('max_weight')
            if 'description' in request.POST:
                section.description = request.POST.get('description')        
            section.save()
            return JsonResponse({'success': True, 'message': 'Section updated successfully'})
        except Section.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Section does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_section(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            section = Section.objects.get(id=id)
            section.delete()
            return JsonResponse({'success': True, 'message': 'Section deleted successfully'})
        except Section.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Section does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})