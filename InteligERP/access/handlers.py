from django.http import JsonResponse
from .models import User,Company,Role
from access.forms import RegisterForm, LoginForm, CreateCompanyForm
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import token_required
import yaml


# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']


def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'User created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, email=email, password=password)
            if user:
                login(request, user)
                # Generar el token JWT
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return JsonResponse({'success': True, 'message': 'User logged in successfully', 'token': token, 'data': user.get_info()})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            # Agrega un mensaje de error personalizado
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

@token_required
def identify_user(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse(user.get_info())

@token_required
def update_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()
    return JsonResponse({'success': True, 'message': 'User updated successfully'})

@token_required
def get_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    return JsonResponse(user.get_info())

@token_required
def get_all_users(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append(user.get_info())
    return JsonResponse({'users': user_list})

@token_required
def update_password(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.set_password(request.POST.get('password'))
    user.save()
    return JsonResponse({'success': True, 'message': 'Password updated successfully'})

@token_required
def delete_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.delete()
    return JsonResponse({'success': True, 'message': 'User deleted successfully'})


# Falta validar que el usuario loggeado sea superuser
@token_required
def adm_update_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.is_superuser = request.POST.get('is_superuser')
    user.is_staff = request.POST.get('is_staff')
    user.save()
    return JsonResponse({'success': True, 'message': 'User updated successfully'})


# Falta validar que el usuario loggeado sea superuser
@token_required
def adm_blank_password(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.set_password('')
    user.save()
    return JsonResponse({'success': True, 'message': 'Password updated successfully'})

@token_required
def create_company(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Company created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_company(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            company = Company.objects.get(id=id)
            return JsonResponse({'id':company.id,
                                 'business_name': company.business_name,
                                 'description': company.description})
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Company does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_company(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        companies_list = []
        for company in companies:
            companies_list.append({'id':company.id,
                                 'business_name': company.business_name,
                                 'description': company.description})
        return JsonResponse({'companies': companies_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_company(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            company = Company.objects.get(id=id)
            if 'business_name' in request.POST:
                company.business_name = request.POST.get('business_name')
            if 'description' in request.POST:
                company.description = request.POST.get('description')      
            company.save()
            return JsonResponse({'success': True, 'message': 'Company updated successfully'})
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Company does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_company(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            company = Company.objects.get(id=id)
            company.delete()
            return JsonResponse({'success': True, 'message': 'Company deleted successfully'})
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Company does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_role(request):   
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            role = Role.objects.get(id=id)
            return JsonResponse({'id':role.id,
                                 'name': role.name})
        except Role.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Role does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_role(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        roles_list = []
        for role in roles:
            roles_list.append({'id':role.id,
                                 'name': role.name})
        return JsonResponse({'roles': roles_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})