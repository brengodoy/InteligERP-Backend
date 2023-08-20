"""
URL configuration for InteligERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from access import handlers

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', handlers.home, name='home'),
    path('register/', handlers.register,
         name='register'),
    path('login/', handlers.login, name='login'),
    path('forgot-password/', handlers.forgot_password, name='forgot-password'),

    # Ver que onda con redirigir páginas del FE con el BE
    path('register-user/', handlers.create_user, name='register-user'),
    path('login-user/', handlers.login_user, name='login-user'),
    path('update-password/', handlers.update_password, name='set-password'),
]
