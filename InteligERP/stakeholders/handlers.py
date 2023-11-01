from django.http import JsonResponse
from stakeholders.models import Supplier, Client
from stakeholders.forms import CreateClientForm, CreateSupplierForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml
import json


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
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'CUIL' in error_dict:
                return JsonResponse({'success': False, 'message': 'CUIL already exists'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_client(request):
    if request.method == 'POST':
        cuil = request.GET.get('CUIL')
        try:
            client = Client.objects.get(CUIL=cuil)
            if 'first_name' in request.POST:
                client.first_name = request.POST.get('first_name')
            if 'last_name' in request.POST:
                client.last_name = request.POST.get('last_name')
            if 'address' in request.POST:
                client.address = request.POST.get('address')
            client.save()
            return JsonResponse({'success': True, 'message': 'Client updated successfully'})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_client(request):
    if request.method == 'GET':
        cuil = request.GET.get('CUIL')
        try:
            client = Client.objects.get(CUIL=cuil)
            return JsonResponse({'first_name': client.first_name,
                                 'last_name': client.last_name,
                                 'address': client.address})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_all_clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        client_list = []
        for client in clients:
            client_list.append({'first_name': client.first_name,
                                'last_name': client.last_name,
                                'address': client.address})
        return JsonResponse({'clients': client_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_client(request):
    if request.method == 'POST':
        cuil = request.POST.get('CUIL')
        try:
            client = Client.objects.get(CUIL=cuil)
            client.delete()
            return JsonResponse({'success': True, 'message': 'Client deleted successfully'})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Client does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def create_supplier(request):
    if request.method == 'POST':
        form = CreateSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Supplier created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'CUIT' in error_dict:
                return JsonResponse({'success': False, 'message': 'CUIT already exists'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def update_supplier(request):
    if request.method == 'POST':
        cuit = request.GET.get('CUIT')
        try:
            supplier = Supplier.objects.get(CUIT=cuit)
            if 'company_name' in request.POST:
                supplier.company_name = request.POST.get('company_name')
            supplier.save()
            return JsonResponse({'success': True, 'message': 'Supplier updated successfully'})
        except Supplier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Supplier does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_supplier(request):
    if request.method == 'GET':
        cuit = request.GET.get('CUIT')
        try:
            supplier = Supplier.objects.get(CUIT=cuit)
            return JsonResponse({'company_name': supplier.company_name,
                                 'CUIT': supplier.CUIT})
        except Supplier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Supplier does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_all_suppliers(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        supplier_list = []
        for supplier in suppliers:
            supplier_list.append({'company_name': supplier.company_name,
                                  'CUIT': supplier.CUIT})
        return JsonResponse({'suppliers': supplier_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_supplier(request):
    if request.method == 'POST':
        cuit = request.POST.get('CUIT')
        try:
            supplier = Supplier.objects.get(CUIT=cuit)
            supplier.delete()
            return JsonResponse({'success': True, 'message': 'Supplier deleted successfully'})
        except Supplier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Supplier does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})