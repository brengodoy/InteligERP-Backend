from django.http import JsonResponse
from stakeholders.models import Supplier,Client
from stakeholders.forms import CreateClientForm, CreateSupplierForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml


# Read YAML configuration file
with open('.config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']


def create_client(request):
    if request.method == 'POST':
        form = CreateClientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Client created successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data'})
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
                         'address': client.address })
                         #'is_superuser': client.is_superuser, 'is_staff': client.is_staff})

def get_all_clients(request):
    clients = Client.objects.all()
    client_list = []
    for client in clients:
        client_list.append({'first_name': client.first_name,
                         	'last_name': client.last_name,
                         	'address': client.address})
    return JsonResponse({'users': client_list})

def delete_client(request):
    client = Client.objects.get(cuil=request.POST.get('CUIL'))
    client.delete()
    return JsonResponse({'success': True, 'message': 'Client deleted successfully'})


# Redirecciona a la página de registro
def register(request):
    return redirect(str(LINK + '/register.html'))


# Redirecciona a la página de login
def login(request):
    return redirect(str(LINK + '/login.html'))


# Redirecciona a la página de forgot password
def forgot_password(request):
    return redirect(str(LINK + '/forgot_password.html'))