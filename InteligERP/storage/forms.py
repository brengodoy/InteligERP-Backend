from django import forms
from storage.models import Warehouse,Section

class CreateWarehouseForm(forms.ModelForm):
    id_warehouse = forms.IntegerField(required=False)  # Hacer el campo de id_warehouse opcional
    description = forms.CharField(required=False)  # Hacer el campo de description opcional
    class Meta:
        model = Warehouse
        fields = ['id_warehouse','name','address','description']

class CreateSectionForm(forms.ModelForm):
    id_section = forms.IntegerField(required=False)  # Hacer el campo de id_section opcional
    description = forms.CharField(required=False)  # Hacer el campo de description opcional
    max_weight = forms.IntegerField(required=False) # Hacer el campo de max_weight opcional
    class Meta:
        model = Section
        fields = ['warehouse','id_section','height','length','width','max_weight','description']