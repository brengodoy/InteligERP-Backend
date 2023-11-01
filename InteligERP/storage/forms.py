from django import forms
from storage.models import Warehouse

class CreateWarehouseForm(forms.ModelForm):
    id_warehouse = forms.IntegerField(required=False)  # Hacer el campo de id_warehouse opcional
    description = forms.CharField(required=False)  # Hacer el campo de description opcional
    class Meta:
        model = Warehouse
        fields = ['id_warehouse','name','address','description']