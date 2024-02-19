from django import forms

from booking.models import Booking

from . models import Payment


class PaymentForm(forms.ModelForm):
    booking = forms.ModelChoiceField(queryset=Booking.objects.filter(status=True).order_by('date_booking'))

    class Meta:
        model = Payment
        fields = "__all__"
        exclude = ['status']
        labels = {
            'date': 'Fecha',
            'payment_method': 'Metodo de pago', 
            'booking': 'reserva', 
            
        }
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
            'payment_method': forms.TextInput(attrs={'placeholder': 'Ingresa el metodo de pago'}),
        }