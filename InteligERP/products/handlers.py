from django.http import JsonResponse
from .models import Object
from .forms import CreateObjectForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml,json
from stakeholders.models import Supplier

# Read YAML configuration file
with open('config.yaml', 'r') as yaml_file:
    LINK = yaml.safe_load(yaml_file).get('default')['LINK']
    
def create_object(request):
    if request.method == 'POST':
        form = CreateObjectForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Object created successfully'})
        else:
            errors = form.errors.as_json()
            error_dict = json.loads(errors) # Convertir JSON a un diccionario de Python
            if 'product_id' in error_dict:
                return JsonResponse({'success': False, 'message': 'The product_id entered already exist.'})
            elif 'supplier' in error_dict:
                return JsonResponse({'success': False, 'message': 'The supplier entered does not exist.'})
            elif 'section' in error_dict:
                return JsonResponse({'success': False, 'message': 'The section entered does not exist.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_object(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            object = Object.objects.get(id=id)
            return JsonResponse({'id':object.id,
                                 'product_id': object.product_id,
                                 'name': object.name,
                                 'height': object.height,
                                 'length': object.length,
                                 'width': object.width,
                                 'weight': object.weight,
                                 'supplier': object.supplier.id,
                                 'section': object.section.id})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_all_objects(request):
    if request.method == 'GET':
        objects = Object.objects.all()
        object_list = []
        for object in objects:
            object_list.append({'id':object.id,
                                 'product_id': object.product_id,
                                 'name': object.name,
                                 'height': object.height,
                                 'length': object.length,
                                 'width': object.width,
                                 'weight': object.weight,
                                 'supplier': object.supplier.id,
                                 'section': object.section.id})
        return JsonResponse({'objects': object_list})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_object(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        try:
            object = Object.objects.get(id=id)
            if 'supplier' in request.POST:
                try:
                    id_supplier = request.POST.get('supplier')
                    supplier = Supplier.objects.get(id=id_supplier)
                    object.supplier = supplier
                except Supplier.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The supplier entered does not exist.'})
            if 'section' in request.POST:
                try:
                    id_section = request.POST.get('section')
                    section = Supplier.objects.get(id=id_section)
                    object.section = section
                except Supplier.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'The section entered does not exist.'})
            if 'product_id' in request.POST:
                object.product_id = request.POST.get('product_id')
            if 'name' in request.POST:
                object.name = request.POST.get('name')
            if 'length' in request.POST:
                object.length = request.POST.get('length')
            if 'width' in request.POST:
                object.width = request.POST.get('width')
            if 'height' in request.POST:
                object.height = request.POST.get('height')
            if 'weight' in request.POST:
                object.weight = request.POST.get('weight')        
            object.save()
            return JsonResponse({'success': True, 'message': 'Object updated successfully'})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_object(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            object = Object.objects.get(id=id)
            object.delete()
            return JsonResponse({'success': True, 'message': 'Object deleted successfully'})
        except Object.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Object does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})