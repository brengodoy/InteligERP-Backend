from django import forms
from stakeholders.models import Supplier,Client

class CreateClientForm(forms.ModelForm):
    address = forms.CharField(required=False)  # Hacer el campo de dirección opcional
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'address', 'CUIL']
        
class CreateSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'CUIT']