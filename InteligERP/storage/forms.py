from django import forms
from storage.models import Warehouse

class CreateWarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['id_warehouse','name','address','description']