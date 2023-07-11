from django.http import JsonResponse
from django.contrib.auth.models import User
from access.forms import RegisterForm, LoginForm


def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return JsonResponse({'success': True, 'message': 'User created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_user(request):
    user = User.objects.get(email=request.GET.get('email'))
    return JsonResponse({'name': user.first_name, 'email': user.email, 'is_superuser': user.is_superuser, 'is_staff': user.is_staff})


def update_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.first_name = request.POST.get('name')
    user.save()
    return JsonResponse({'success': True, 'message': 'User updated successfully'})


def delete_user(request):
    user = User.objects.get(email=request.POST.get('email'))
    user.delete()
    return JsonResponse({'success': True, 'message': 'User deleted successfully'})


def get_all_users(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({'name': user.first_name, 'email': user.email,
                          'is_superuser': user.is_superuser, 'is_staff': user.is_staff})
    return JsonResponse({'users': user_list})


# def register(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         print('#####1', form)
#         if form.is_valid():
#             print('#####2', form)
#             try:
#                 form.save()
#                 return redirect('/index')
#             except:
#                 pass
#     else:
#         print('#####3', form)
#         form = UserForm()
#     return render(request, 'access/templates/register.html', {'form': form})


def login(request):
    if request.method == "GET":
        form = UserForm(request.GET)
        print('#####1', form)
    else:
        form = UserForm()
        print('#####2', form)
    return render(request, 'access/templates/login.html', {'form': form})


# def emp(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/show')
#             except:
#                 pass
#     else:
#         form = EmployeeForm()
#     return render(request,'index.html',{'form':form})

# def show(request):
#     employees = Employee.objects.all()
#     return render(request, "show.html", {'employees': employees})


# def edit(request, id):
#     employee = Employee.objects.get(id=id)
#     return render(request, 'edit.html', {'employee': employee})


# def update(request, id):
#     employee = Employee.objects.get(id=id)
#     form = EmployeeForm(request.POST, instance=employee)
#     if form.is_valid():
#         form.save()
#         return redirect("/show")
#     return render(request, 'edit.html', {'employee': employee})


# def destroy(request, id):
#     employee = Employee.objects.get(id=id)
#     employee.delete()
#     return redirect("/show")
