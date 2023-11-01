from django.http import JsonResponse
from storage.models import Warehouse
from storage.forms import CreateWarehouseForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml

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
        warehouse_id = request.GET.get('id_warehouse')
        try:
            warehouse = Warehouse.objects.get(id_warehouse=warehouse_id)
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
"""def update_warehouse(request):
    if request.method == 'PUT':
        warehouse_id = request.GET.get('id_warehouse')
        try:
               warehouse = Warehouse.objects.get(id_warehouse=warehouse_id)
               warehouse.name = request.GET.get('name')
               warehouse.address = request.GET.get('address')
               warehouse.description = request.GET.get('description')
               warehouse.save()
               return JsonResponse({'success': True, 'message': 'Warehouse updated successfully'})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})"""

def get_warehouse(request):
    if request.method == 'GET':
        warehouse_id = request.GET.get('id_warehouse')
        try:
            warehouse = Warehouse.objects.get(id_warehouse=warehouse_id)
            return JsonResponse({'name': warehouse.name,
                                 'address': warehouse.address,
                                 'description': warehouse.description})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

"""def get_warehouse(request):
    warehouse = Warehouse.objects.get(id_warehouse=request.POST.get('id_warehouse'))
    return JsonResponse({'name': warehouse.name,
                         'address': warehouse.address,
                         'description': warehouse.description})"""

def get_all_warehouses(request):
    warehouses = Warehouse.objects.all()
    warehouse_list = []
    for warehouse in warehouses:
        warehouse_list.append({'name': warehouse.name,
                         	   'address': warehouse.address,
                         	   'description': warehouse.description})
    return JsonResponse({'users': warehouse_list})

def delete_warehouse(request):
    if request.method == 'POST':
        id_warehouse = request.POST.get('id_warehouse')
        try:
            warehouse = Warehouse.objects.get(cuil=id_warehouse)
            warehouse.delete()
            return JsonResponse({'success': True, 'message': 'Warehouse deleted successfully'})
        except Warehouse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Warehouse does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})