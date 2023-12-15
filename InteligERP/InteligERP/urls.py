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
from products import handlers as objects
from transactions import handlers as transactions
from dashboards import handlers as dashboards

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', access.admin),

    path('signup/', access.create_user, name='signup'),
    path('me/', access.identify_user, name='me'),
    path('signin/', access.login_user, name='login_user'),
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
	
    path('create-object/', objects.create_object, name='create-object'),
	path('get-object/', objects.get_object, name='get-object'),
	path('get-all-objects/', objects.get_all_objects, name='get-all-objects'),
	path('update-object/', objects.update_object, name='update-object'),
	#path('delete-object/', objects.delete_object, name='delete-object'),
	
    path('create-price/', objects.create_price, name='create-price'),
	path('get-price/', objects.get_price, name='get-price'),
	path('delete-price/', objects.delete_price, name='delete-price'),
	
    path('create-sale/', transactions.create_sale, name='create-sale'),
	path('get-sale/', transactions.get_sale, name='get-sale'),
	path('get-all-sales/', transactions.get_all_sales, name='get-all-sales'),
	path('update-sale/', transactions.update_sale, name='update-sale'),
	path('delete-sale/', transactions.delete_sale, name='delete-sale'),

    path('create-sale-object/', transactions.create_sale_object, name='create-sale-object'),
	path('get-sale-object/', transactions.get_sale_object, name='get-sale-object'),
	path('get-all-sale-object/', transactions.get_all_sale_object, name='get-sale-all-object'),
	path('update-sale-object/', transactions.update_sale_object, name='update-sale-object'),
	path('delete-sale-object/', transactions.delete_sale_object, name='delete-sale-object'),
	
    path('create-purchase/', transactions.create_purchase, name='create-purchase'),
	path('get-purchase/', transactions.get_purchase, name='get-purchase'),
	path('get-all-purchase/', transactions.get_all_purchase, name='get-all-purchase'),
	path('update-purchase/', transactions.update_purchase, name='update-purchase'),
	path('delete-purchase/', transactions.delete_purchase, name='delete-purchase'),
	
	path('create-purchase-object/', transactions.create_purchase_object, name='create-purchase-object'),
	path('get-purchase-object/', transactions.get_purchase_object, name='get-purchase-object'),
	path('get-all-purchase-object/', transactions.get_all_purchase_object, name='get-all-purchase-object'),
	path('update-purchase-object/', transactions.update_purchase_object, name='update-purchase-object'),
	path('delete-purchase-object/', transactions.delete_purchase_object, name='delete-purchase-object'),
	
    path('create-company/', access.create_company, name='create-company'),
	path('get-company/', access.get_company, name='get-company'),
	path('get-all-company/', access.get_all_company, name='get-all-company'),
	path('update-company/', access.update_company, name='update-company'),
	path('delete-company/', access.delete_company, name='delete-company'),	
	
    path('get-role/', access.get_role, name='get-role'),
	path('get-all-role/', access.get_all_role, name='get-all-role'),

	path('create-dashboard/', dashboards.create_dashboard, name='create-dashboard'),
]
