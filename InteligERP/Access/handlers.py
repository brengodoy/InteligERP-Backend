from django.http import JsonResponse
from django.contrib.auth.models import User
from access.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login


def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return JsonResponse({'success': True, 'message': 'User created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'User logged in successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    return JsonResponse({'name': user.first_name, 'email': user.email,
                         'is_superuser': user.is_superuser, 'is_staff': user.is_staff})


def get_all_users(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({'name': user.first_name, 'email': user.email,
                          'is_superuser': user.is_superuser, 'is_staff': user.is_staff})
    return JsonResponse({'users': user_list})


def update_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()
    return JsonResponse({'success': True, 'message': 'User updated successfully'})


def update_password(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.set_password(request.POST.get('password'))
    user.save()
    return JsonResponse({'success': True, 'message': 'Password updated successfully'})


def delete_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.delete()
    return JsonResponse({'success': True, 'message': 'User deleted successfully'})


# Falta validar que el usuario loggeado sea superuser
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
def adm_blank_password(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.set_password('')
    user.save()
    return JsonResponse({'success': True, 'message': 'Password updated successfully'})
