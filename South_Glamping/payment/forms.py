from django import forms
from . models import Payment

from booking.models import Booking

class PaymentForm(forms.ModelForm):
    booking = forms.ModelChoiceField(queryset=Booking.objects.order_by('customer'))

    class Meta:
        model = Payment
        fields = "__all__"
        exclude = ['',]
        
        labels = {
            'date': 'Fecha',
            'payment_method': 'Método de pago', 
            'booking': 'Reserva',
            'status' : 'Estado' 
            
        }
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
            'payment_method': forms.TextInput(attrs={'placeholder': 'Ingresa el método de pago'}),
            'status': forms.TextInput(attrs={'placeholder': 'Ingresa el estado del pago'}),
        }