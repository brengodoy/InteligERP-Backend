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
from access import handlers as access
from stakeholders import handlers as stakeholders
from storage import handlers as storage

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', access.admin),

    path('signup/', access.create_user, name='signup'),
    path('me', access.identify_user, name='me'),
    path('signin', access.login_user, name='login_user'),

    path('update-password/', access.update_password, name='set-password'),

    path('create-client/', stakeholders.create_client, name='create-client'),
    path('update-client/', stakeholders.update_client, name='update-client'),
    path('get-client/', stakeholders.get_client, name='get-client'),
    path('get-all-clients/', stakeholders.get_all_clients, name='get-all-clients'),
	path('delete-client/', stakeholders.delete_client, name='delete-client'),

    path('create-supplier/', stakeholders.create_supplier, name='create-supplier'),
    path('update-supplier/', stakeholders.update_supplier, name='update-supplier'),
    path('get-supplier/', stakeholders.get_supplier, name='get-supplier'),
    path('get-all-suppliers/', stakeholders.get_all_suppliers,name='get-all-supplier'),
    path('delete-supplier/', stakeholders.delete_supplier,name='delete-supplier'),
		 
    path('create-warehouse/', storage.create_warehouse, name='create-warehouse'),
    path('update-warehouse/', storage.update_warehouse, name='update-warehouse'),
    path('get-warehouse/', storage.get_warehouse, name='get-warehouse'),
    path('get-all-warehouses/', storage.get_all_warehouses,name='get-all-warehouses'),
    path('delete-warehouse/', storage.delete_warehouse,name='delete-warehouse'),
	
    path('create-section/', storage.create_section, name='create-section'),
	path('get-section/', storage.get_section, name='get-section'),
	path('get-all-sections/', storage.get_all_sections, name='get-all-sections'),
	path('update-section/', storage.update_section, name='update-section'),
	path('delete-section/', storage.delete_section, name='delete-section'),

]
