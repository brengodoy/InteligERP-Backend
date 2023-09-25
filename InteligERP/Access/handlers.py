from django.http import JsonResponse
from .models import User
from access.forms import RegisterForm, LoginForm
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
