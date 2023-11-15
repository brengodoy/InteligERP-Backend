from django.http import JsonResponse
from .forms import CreateSaleForm,CreatePurchaseForm,CreateSaleObjectForm,CreatePurchaseObjectForm
import yaml,json
from .models import Sale,Sale_object,Object,Purchase,Purchase_object
from stakeholders.models import Client,Supplier
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from products.models import Price
from django.db.models import Max,Sum
from decimal import Decimal

# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']

def create_sale(request):
    if request.method == 'POST':
        form = CreateSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Sale created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'client' in error_dict:
                return JsonResponse({'success': False, 'message': 'The client entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_sale(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            sale = Sale.objects.get(id=id)
            return JsonResponse({'id':sale.id,
                                 'date': sale.date,
                                 'paid': sale.paid,
                                 'client': sale.client.id})
        except Sale.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_sales(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        sale_list = []
        for sale in sales:
            sale_list.append({'id':sale.id,
                                 'date': sale.date,
                                 'paid': sale.paid,
                                 'client': sale.client.id})
        return JsonResponse({'sales': sale_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_sale(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            sale = Sale.objects.get(id=id)
            if 'client' in request.POST:
                try:
                    id_client = request.POST.get('client')
                    client = Client.objects.get(id=id_client)
                    sale.client = client
                except Client.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The client entered does not exist.'})
            if 'date' in request.POST:
                sale.date = request.POST.get('date')
            if 'paid' in request.POST:
                sale.paid = request.POST.get('paid')      
            sale.save()
            return JsonResponse({'success': True, 'message': 'Sale updated successfully'})
        except Sale.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_sale(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            sale = Sale.objects.get(id=id)
            sale_objects = Sale_object.objects.filter(sale=id)
            sale_objects.delete()
            sale.delete()
            return JsonResponse({'success': True, 'message': 'Sale deleted successfully'})
        except Sale.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def create_sale_object(request):
    if request.method == 'POST':
        form = CreateSaleObjectForm(request.POST)
        if form.is_valid():
            sale_object = form.save(commit=False)
            if sale_object.object.discontinued == False:
                form.save()
                calculate_stock(sale_object.object.id)
                return JsonResponse({'success': True, 'message': 'Sale_object created successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'The object entered is discontinued.'})            
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if '__all__' in error_dict:
                return JsonResponse({'success': False, 'message': 'The object entered is already in this sale.'})
            elif 'sale' in error_dict:
                return JsonResponse({'success': False, 'message': 'The sale entered does not exist.'})
            elif 'object' in error_dict:
                return JsonResponse({'success': False, 'message': 'The object entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_sale_object(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            sale_object = Sale_object.objects.get(id=id)
            return JsonResponse({'id':sale_object.id,
                                 'sale': sale_object.sale.id,
                                 'object': sale_object.object.id,
                                 'amount': sale_object.amount})
        except Sale_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale_object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_sale_object(request):
    if request.method == 'GET':
        sales_objects = Sale_object.objects.all()
        sales_objects_list = []
        for sale_object in sales_objects:
            sales_objects_list.append({'id':sale_object.id,
                                 'sale': sale_object.sale.id,
                                 'object': sale_object.object.id,
                                 'amount': sale_object.amount})
        return JsonResponse({'sales': sales_objects_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_sale_object(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            sale_object = Sale_object.objects.get(id=id)
            if 'sale' in request.POST:
                try:
                    id_sale = request.POST.get('sale')
                    sale = Sale.objects.get(id=id_sale)
                    sale_object.sale = sale
                except Sale.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The sale entered does not exist.'})
            if 'amount' in request.POST and 'object' in request.POST:
                id_object = request.POST.get('object')
                old_object_id = sale_object.object.id
                object = Object.objects.get(id=id_object)
                if object.discontinued == False:
                    sale_object.object = object
                    sale_object.amount = request.POST.get('amount')
                    sale_object.save()
                    calculate_stock(id_object)
                    calculate_stock(old_object_id)
                else:
                    return JsonResponse({'success': False, 'message': 'The object entered is discontinued.'})
            else:
                if 'amount' in request.POST:
                    sale_object.amount = request.POST.get('amount')
                    sale_object.object.stock = Decimal(sale_object.object.stock) - Decimal(sale_object.amount)
                    sale_object.object.save() 
                    sale_object.save()
                    calculate_stock(sale_object.object.id)
                if 'object' in request.POST:
                    try:
                        id_object = request.POST.get('object')
                        object = Object.objects.get(id=id_object)
                        old_object_id = sale_object.object.id
                        if object.discontinued == False:
                            sale_object.object = object
                            sale_object.save()
                            calculate_stock(id_object)
                            calculate_stock(old_object_id)
                        else:
                            return JsonResponse({'success': False, 'message': 'The object entered is discontinued.'})
                    except Object.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'The object entered does not exist.'})      
            sale_object.save()
            return JsonResponse({'success': True, 'message': 'Sale_object updated successfully'})
        except Sale_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale_object does not exist'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'The object entered is already in this sale.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_sale_object(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            sale_object = Sale_object.objects.get(id=id)
            sale_object.delete()
            calculate_stock(sale_object.object.id)
            return JsonResponse({'success': True, 'message': 'Sale_object deleted successfully'})
        except Sale_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale_object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def create_purchase(request):
    if request.method == 'POST':
        mutable_post = request.POST.copy()  # Crea una copia mutable del objeto request.POST
        mutable_post['total_cost'] = 0
        form = CreatePurchaseForm(mutable_post)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Purchase created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'supplier' in error_dict:
                return JsonResponse({'success': False, 'message': 'The supplier entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_purchase(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            purchase = Purchase.objects.get(id=id)
            return JsonResponse({'id':purchase.id,
                                 'date': purchase.date,
                                 'total_cost': purchase.total_cost,
                                 'supplier': purchase.supplier.id})
        except Purchase.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_purchase(request):
    if request.method == 'GET':
        purchases = Purchase.objects.all()
        purchase_list = []
        for purchase in purchases:
            purchase_list.append({'id':purchase.id,
                                 'date': purchase.date,
                                 'total_cost': purchase.total_cost,
                                 'supplier': purchase.supplier.id})
        return JsonResponse({'purchases': purchase_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_purchase(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            purchase = Purchase.objects.get(id=id)
            if 'supplier' in request.POST:
                try:
                    id_supplier = request.POST.get('supplier')
                    supplier = Supplier.objects.get(id=id_supplier)
                    purchase.supplier = supplier
                except Supplier.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The supplier entered does not exist.'})
            if 'date' in request.POST:
                purchase.date = request.POST.get('date')      
            purchase.save()
            return JsonResponse({'success': True, 'message': 'Purchase updated successfully'})
        except Purchase.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_purchase(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            purchase = Purchase.objects.get(id=id)
            purchase_objects = Purchase_object.objects.filter(purchase=purchase)
            purchase_objects.delete()
            purchase.delete()
            return JsonResponse({'success': True, 'message': 'Purchase deleted successfully'})
        except Purchase.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def create_purchase_object(request):
    if request.method == 'POST':
        form = CreatePurchaseObjectForm(request.POST)
        if form.is_valid():
            purchase_object = form.save(commit=False)
            if purchase_object.object.discontinued == False:
                purchase = Purchase.objects.get(id=request.POST.get('purchase'))
                object = Object.objects.get(id=request.POST.get('object'))
                #object.stock = object.stock + Decimal(request.POST.get('amount'))
                #object.save()
                price = Price.objects.filter(object=object.id, supplier=purchase.supplier.id, date__lt=purchase.date).order_by('-date').first()
                purchase_object.price = Decimal(purchase_object.amount) * Decimal(price.price)
                purchase_object.save()
                calculate_total_cost(purchase.id)
                calculate_stock(object.id)
            else:
                return JsonResponse({'success': False, 'message': 'The object entered is discontinued.'})
            return JsonResponse({'success': True, 'message': 'Purchase_object created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'purchase' in error_dict:
                return JsonResponse({'success': False, 'message': 'The purchase entered does not exist.'})
            elif 'object' in error_dict:
                return JsonResponse({'success': False, 'message': 'The object entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_purchase_object(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            purchase_object = Purchase_object.objects.get(id=id)
            return JsonResponse({'id': purchase_object.id,
                                 'purchase': purchase_object.purchase.id,
                                 'object': purchase_object.object.id,
                                 'amount': purchase_object.amount,
                                 'price': purchase_object.price})
        except Purchase_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase_object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_purchase_object(request):
    if request.method == 'GET':
        if 'id_purchase' in request.GET:
            try:
                purchase = Purchase.objects.get(id=request.GET.get('id_purchase'))
                purchase_objects = Purchase_object.objects.filter(purchase=purchase)
            except Purchase.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Purchase entered does not exist'})
        else:
            purchase_objects = Purchase_object.objects.all()
        
        purchase_object_list = []
        for purchase_object in purchase_objects:
            purchase_object_list.append({
                'id': purchase_object.id,
                'purchase': purchase_object.purchase.id,
                'object': purchase_object.object.id,
                'amount': purchase_object.amount,
                'price': purchase_object.price
            })
        return JsonResponse({'purchase_objects': purchase_object_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_purchase_object(request):
    if request.method == 'POST':
        id_purchase_object = request.GET.get('id_purchase_object')
        try:
            purchase_object = Purchase_object.objects.get(id=id_purchase_object)
            if 'amount' in request.POST:
                purchase_object.amount = request.POST.get('amount')
                purchase_object.save()
                calculate_stock(purchase_object.object.id)
                calculate_price(id_purchase_object,request.POST.get('amount'))
            return JsonResponse({'success': True, 'message': 'Purchase_object updated successfully'})
        except Purchase_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase_object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_purchase_object(request):
    if request.method == 'DELETE':
        id_purchase_object = request.GET.get('id_purchase_object')
        try:
            purchase_object = Purchase_object.objects.get(id=id_purchase_object)
            purchase_object.delete()
            calculate_total_cost(purchase_object.purchase.id)
            calculate_stock(purchase_object.object.id)
            return JsonResponse({'success': True, 'message': 'Purchase deleted successfully'})
        except Purchase_object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase_object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def calculate_total_cost(id_purchase):
    purchase = Purchase.objects.get(id=id_purchase)
    purchase_objects = Purchase_object.objects.filter(purchase=purchase.id)
    total_price_sum = purchase_objects.aggregate(total_price_sum=Sum('price'))
    total_cost = total_price_sum.get('total_price_sum', 0) or Decimal('0.0')
    purchase.total_cost = total_cost
    purchase.save()

def calculate_price(id_purchase_object,amount):
    purchase_object = Purchase_object.objects.get(id=id_purchase_object)
    purchase = Purchase.objects.get(id=purchase_object.purchase.id)
    object = Object.objects.get(id=purchase_object.object.id)
    price = Price.objects.filter(object=object, supplier=purchase.supplier, date__lt=purchase.date).order_by('-date').first()
    purchase_object.price = Decimal(amount) * Decimal(price.price)
    purchase_object.save()
    calculate_total_cost(purchase.id)
    
def calculate_stock(id_object):
    object = Object.objects.get(id=id_object)
    purchase_objects = Purchase_object.objects.filter(object=object)
    sale_objects = Sale_object.objects.filter(object=object)
    acquired = 0
    sold = 0
    for purchase_object in purchase_objects:
        acquired = acquired + purchase_object.amount
    for sale_object in sale_objects:
        sold = sold + sale_object.amount
    object.stock = acquired - sold
    object.save()