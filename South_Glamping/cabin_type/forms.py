from django import forms
from . models import Cabin_type

class Cabin_typeForm(forms.ModelForm):
    class Meta:
        model = Cabin_type
        fields = "__all__"
        exclude = ['status']
        labels = {
            'image': 'Imagen',
            'name': 'Nombre',
            'description': 'Descripción',
            'status': 'Estado',                    
        }
        widgets = {
            'image': forms.FileInput(attrs={'placeholder': 'Ingrese la imagen del tipo de cabaña'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ingresa la descripción'}),
            'status': forms.TextInput(attrs={'placeholder': 'Ingresa el Estado'}),           
        }