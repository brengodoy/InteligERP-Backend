from django.http import JsonResponse
from .forms import CreateSaleForm,CreatePurchaseForm
import yaml,json
from .models import Sale
from stakeholders.models import Client

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
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            sale = Sale.objects.get(id=id)
            sale.delete()
            return JsonResponse({'success': True, 'message': 'Sale deleted successfully'})
        except Sale.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sale does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})