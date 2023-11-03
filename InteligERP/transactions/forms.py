from django import forms
from .models import Sale,Purchase

class CreateSaleForm(forms.ModelForm):
    date = forms.DateTimeField(required=False)  # Hacer el campo de date opcional
    paid = forms.BooleanField(required=False)  # Hacer el campo de paid opcional
    class Meta:
        model = Sale
        fields = ['date','paid','client']

class CreatePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date','total_cost','supplier']