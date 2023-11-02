from django.http import JsonResponse
from .models import Object
from .forms import CreateObjectForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import yaml,json

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
            else:
	            return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})