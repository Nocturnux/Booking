from django.shortcuts import render, redirect
from payment.models import Payment
from .forms import PaymentForm
from django.http import JsonResponse
from django.contrib import messages


def payment(request):    
    payment_list = Payment.objects.all()    
    return render(request, 'payment/index.html', {'payment_list': payment_list})

def create_payment(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payment')   
    print(form.errors) 
    return render(request, 'payment/create.html', {'form': form})

def detail_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    data = { 'date': payment.date, 'payment_method': payment.payment_method, 'status': payment.status }    
    return JsonResponse(data)

def edit_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    form = PaymentForm(request.POST or None, request.FILES or None, instance=payment)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Pago actualizado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar el pago.')
        return redirect('payment')    
    return render(request, 'payment/edit.html', {'form': form})