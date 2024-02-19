from django import forms
from . models import Cabin

from cabin_type.models import Cabin_type

class CabinForm(forms.ModelForm):
    cabin_type = forms.ModelChoiceField(queryset=Cabin_type.objects.filter(status=True).order_by('name'))
    
    class Meta:
        model = Cabin
        fields = "__all__"
        exclude = ['status',]
        
        labels = {
            'name': 'Nombre',
            'image': 'Imagen',
            'capacity': 'Capacidad',
            'description': 'Descripción',
            'cabin_type': 'Tipo de cabaña',
            'price': 'valor',                                   
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la cabaña'}),
            'image': forms.FileInput(attrs={'placeholder': 'Ingrese la imagen de la cabaña'}),
            'capacity': forms.TextInput(attrs={'placeholder': 'Ingrese la capacidad de la cabaña'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese la descripción de la cabaña'}), 
            'price': forms.NumberInput(attrs={'placeholder': 'Ingrese el valor de la cabaña'}),
        }