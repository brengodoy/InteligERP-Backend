from django.http import JsonResponse
from transactions.models import Sale_object,Sale,Purchase_object
from datetime import timedelta
from decimal import Decimal
from django.db.models import ExpressionWrapper, F, DecimalField

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
    
    stock_changes = calculate_stock_changes_in_range(start_date, end_date, id_object)

	# Crear el diccionario de respuesta
    response_data = {
        'sell_line_chart': {
            'title': 'Sales',
            'data': sales_data,
        },
        'stock_status': {
			'title': 'Stock',
			'data': stock_changes,
		}
    }

    return JsonResponse(response_data)

def calculate_stock_changes_in_range(start_date, end_date, id_object):
    # Obtener las compras y ventas en el rango de fechas
    purchases = Purchase_object.objects.filter(
        purchase__date__range=[start_date, end_date],
        object__id=id_object
    ).annotate(change=ExpressionWrapper(F('amount'), output_field=DecimalField()))

    sales = Sale_object.objects.filter(
        sale__date__range=[start_date, end_date],
        object__id=id_object
    ).annotate(change=ExpressionWrapper(F('amount') * Decimal('-1'), output_field=DecimalField()))

    # Combinar compras y ventas
    changes = list(purchases) + list(sales)
    
	# Ordenar los cambios por fecha
    #print('IMPRIMIR: ',changes)
    changes.sort(key=lambda obj: obj.purchase.date if isinstance(obj, Purchase_object) else obj.sale.date)
    #changes.sort(key=lambda obj: obj.purchase.date if hasattr(obj, 'purchase') else obj.sale.date)
    
    # Calcular el stock acumulado para cada fecha
    current_stock = 0
    stock_changes = []

    """for change in changes:
        current_stock += change.change
        stock_changes.append({'date': change.sale.date.strftime('%d-%m-%Y'), 'stock': current_stock})"""
    for change in changes:
        if isinstance(change, Purchase_object):
            date = change.purchase.date
            amount_change = change.amount
        elif isinstance(change, Sale_object):
            date = change.sale.date
            amount_change = change.amount * Decimal('-1')
            
        current_stock += amount_change
        stock_changes.append({'date': date.strftime('%d-%m-%Y'), 'stock': current_stock})

    return stock_changes