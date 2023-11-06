from django import forms
from .models import Sale,Purchase,Sale_object,Purchase_object
from django.utils import timezone

class CreateSaleForm(forms.ModelForm):
    date = forms.DateTimeField(required=False)  # Hacer el campo de date opcional
    paid = forms.BooleanField(required=False)  # Hacer el campo de paid opcional
    class Meta:
        model = Sale
        fields = ['date','paid','client']

class CreateSaleObjectForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=20,decimal_places=2,required=False)  # Hacer el campo de amount opcional
    class Meta:
        model = Sale_object
        fields = ['sale','object','amount']

class CreatePurchaseForm(forms.ModelForm):
    total_cost = forms.DecimalField(max_digits=20,decimal_places=2,required=False)  # Hacer el campo de total_cost opcional
    date = forms.DateTimeField(required=False)  # Hacer el campo de date opcional
    class Meta:
        model = Purchase
        fields = ['date','total_cost','supplier']
        
class CreatePurchaseObjectForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=20,decimal_places=2,required=False)  # Hacer el campo de amount opcional
    price = forms.DecimalField(max_digits=20,decimal_places=2,required=False)  # Hacer el campo de price opcional)
    class Meta:
        model = Purchase_object
        fields = ['purchase','object','amount','price']