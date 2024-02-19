from django import forms
from . models import Cabin_type

class Cabin_typeForm(forms.ModelForm):
    class Meta:
        model = Cabin_type
        fields = "__all__"
        exclude = ['status']
        labels = {
            'name': 'Nombre',
            'status': 'Estado',                    
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre'}),
            'status': forms.TextInput(attrs={'placeholder': 'Ingresa el Estado'}),           
        }