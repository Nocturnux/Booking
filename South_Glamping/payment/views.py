from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from datetime import datetime
from payment.models import Payment
from booking.models import Booking
from .forms import PaymentForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import View
from django.contrib.staticfiles import finders


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
def payment(request):    
    payment_list = Payment.objects.all()    
    return render(request, 'payment/index.html', {'payment_list': payment_list})

@login_required
@user_passes_test(admin_or_staff)
def create_payment(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        payment_instance = form.save()  # Guarda el formulario y obtén la instancia de Payment
        booking_instance = payment_instance.booking  # Obtén la instancia de Booking asociada al Payment
        booking_instance.status = 'Confirmado'  # Establece el estado como 'Reservado'
        booking_instance.save()  # Guarda los cambios en la instancia de Booking
        return redirect('payment')   
    print(form.errors) 
    return render(request, 'payment/create.html', {'form': form})

@login_required
@user_passes_test(admin_or_staff)
def detail_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    data = { 'amount' : payment.amount, 'date': payment.date, 'payment_method': payment.payment_method, 'status': payment.status }    
    return JsonResponse(data)

@login_required
@user_passes_test(admin_or_staff)
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

""" class ReportInvoicePdfView(View):
    def get(self, request, *args, **kwargs ):
        template = get_template('booking/invoice.html')
        context = {'title' : 'pdf'}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report_payment.pdf"' 
        pisaStatus = pisa.CreatePDF(
            html, dest=response)
        if pisaStatus.err:
            return HttpResponse(' Hay un error ' + html)
        return response """

