from django import forms
from . models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['status']
        labels = {
            'name': 'Nombre',
            'document': 'Documento',
            'cellphone': 'Celular',
            'status': 'Estado',                      
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre'}),
            'document': forms.TextInput(attrs={'placeholder': 'Ingresa el documento'}),
            'cellphone': forms.TextInput(attrs={'placeholder': 'Ingresa el celular'}),
            'status': forms.TextInput(attrs={'placeholder': 'Ingresa el estado'}),          
        }