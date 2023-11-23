from django.http import JsonResponse
from transactions.models import Sale_object,Sale

def create_dashboard(request):
    start_date = request.GET.get('start_date')
    end_date= request.GET.get('end_date')
    id_object= request.GET.get('id_object')
    
	# 1. Filtrar las ventas dentro del rango de fechas
    sales = Sale.objects.filter(date__range=[start_date, end_date])

	# 2. Obtener los Sale_object asociados a esas ventas y al objeto específico
    sale_objects = Sale_object.objects.filter(sale__in=sales, object__id=id_object)
    
    sales_data = [
        {'date': sale_object.sale.date.strftime('%d-%m-%Y'), 'value': sale_object.amount}
        for sale_object in sale_objects
    ]

	# Crear el diccionario de respuesta
    response_data = {
        'sell_line_chart': {
            'title': 'Ventas',
            'data': sales_data,
        },
        # Resto de la respuesta...
    }

    return JsonResponse(response_data)