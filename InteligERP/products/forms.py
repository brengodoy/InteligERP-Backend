from django import forms
from .models import Object,Price

class CreateObjectForm(forms.ModelForm):
    #product_id = forms.IntegerField(required=False)  # Hacer el campo de product_id opcional
    discontinued = forms.BooleanField(required=False)   # Hacer el campo de discontinued opcional

    class Meta:
        model = Object
        fields = ['name','height','length','width','weight','section','discontinued','stock']

class CreatePriceForm(forms.ModelForm):
    currency = forms.CharField(required=False)  # Hacer el campo de currency opcional
    date = forms.DateTimeField(required=False)  # Hacer el campo de date opcional

    class Meta:
        model = Price
        fields = ['object','price','date','currency','supplier']