from django import forms
from .models import Object

class CreateObjectForm(forms.ModelForm):
    product_id = forms.IntegerField(required=False)  # Hacer el campo de product_id opcional

    class Meta:
        model = Object
        fields = ['product_id','name','height','length','width','weight']