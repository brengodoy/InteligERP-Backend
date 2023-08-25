from django.http import JsonResponse
from stakeholders.models import Supplier, Client
from stakeholders.forms import CreateClientForm, CreateSupplierForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml


# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']


def create_client(request):
    if request.method == 'POST':
        form = CreateClientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Client created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def update_client(request):
    client = Client.objects.get(cuil=request.POST.get('CUIL'))
    client.first_name = request.POST.get('first_name')
    client.last_name = request.POST.get('last_name')
    client.address = request.POST.get('address')
    client.save()
    return JsonResponse({'success': True, 'message': 'Client updated successfully'})


def get_client(request):
    client = Client.objects.get(cuil=request.POST.get('CUIL'))
    return JsonResponse({'first_name': client.first_name,
                         'last_name': client.last_name,
                         'address': client.address})


def get_all_clients(request):
    clients = Client.objects.all()
    client_list = []
    for client in clients:
        client_list.append({'first_name': client.first_name,
                            'last_name': client.last_name,
                            'address': client.address})
    return JsonResponse({'users': client_list})


def create_supplier(request):
    if request.method == 'POST':
        form = CreateSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Supplier created successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def update_supplier(request):
    supplier = Supplier.objects.get(cuit=request.POST.get('CUIT'))
    supplier.company_name = request.POST.get('company_name')
    supplier.save()
    return JsonResponse({'success': True, 'message': 'Supplier updated successfully'})


def get_supplier(request):
    supplier = Supplier.objects.get(cuit=request.POST.get('CUIT'))
    return JsonResponse({'company_name': supplier.company_name,
                         'CUIT': supplier.cuit})


def get_all_suppliers(request):
    suppliers = Supplier.objects.all()
    supplier_list = []
    for supplier in suppliers:
        supplier_list.append({'company_name': supplier.company_name,
                              'CUIT': supplier.cuit})
    return JsonResponse({'users': supplier_list})
