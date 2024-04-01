from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from customer.models import Customer
from cabin.models import Cabin
from service.models import Service
from booking.models import Booking
from booking_cabin.models import Booking_cabin
from booking_service.models import Booking_service
from payment.models import Payment
from django.db import models
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
def booking(request):    
    booking_list = Booking.objects.all()    
    return render(request, 'booking/index.html', {'booking_list': booking_list})


@login_required
def create_booking(request):
    customer_list = Customer.objects.all()
    cabin_list = Cabin.objects.all()
    service_list = Service.objects.all()    
    
    if request.method == 'POST':
        date_start_str = request.POST['date_start']
        date_end_str = request.POST['date_end']        
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d')
        
    
    
        booking = Booking.objects.create(                        
            date_booking=datetime.now().date(),                                   
            date_start=date_start,
            date_end=date_end,
            price=request.POST['totalValueUnformatted'],
            status='Reservado',
            customer_id=request.POST['customer']
        )
        booking.save()        
        cabin_Id = request.POST.getlist('cabinId[]')
        service_Id = request.POST.getlist('serviceId[]')
        cabin_price = request.POST.getlist('cabinPrice[]')
        service_price = request.POST.getlist('servicePrice[]') 
            
                
        for i in range(len(cabin_Id)):            
            cabin = Cabin.objects.get(pk=int(cabin_Id[i]))
            booking_cabin = Booking_cabin.objects.create(
                booking=booking,
                cabin=cabin,
                price=cabin_price[i]
            )
            booking_cabin.save()
        
        for i in range(len(service_Id)):
                service = Service.objects.get(pk=int(service_Id[i]))
                booking_service = Booking_service.objects.create(
                    booking=booking,
                    service=service,
                    price=service_price[i]
                )
                booking_service.save()      
            
                    
        messages.success(request, 'Reserva creada con éxito.')
        return redirect('booking')
    
    return render(request, 'booking/create.html', {'customer_list': customer_list, 'cabin_list': cabin_list, 'service_list': service_list})


@login_required
def detail_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking_cabin = Booking_cabin.objects.filter(booking=booking)
    booking_service = Booking_service.objects.filter(booking=booking)
    payment = Payment.objects.filter(booking=booking)
    return render(request, 'booking/detail.html', {'booking': booking, 'booking_cabin': booking_cabin, 'booking_service': booking_service, 'payment': payment})


@login_required
@user_passes_test(admin_or_staff)
def delete_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    try:
        booking.delete()        
        messages.success(request, 'Reserva eliminada correctamente.')
    except:
        messages.error(request, 'No se puede eliminar la reserva porque está asociada a un servicio.')
    return redirect('booking')




@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    customer_list = Customer.objects.all()
    cabin_list = Cabin.objects.all()
    service_list = Service.objects.all()
    booking_cabin = Booking_cabin.objects.filter(booking=booking)
    booking_service = Booking_service.objects.filter(booking=booking)
    
    if request.method == 'POST':
        # Eliminar los detalles de la reserva existente
        Booking_cabin.objects.filter(booking=booking).delete()
        Booking_service.objects.filter(booking=booking).delete()
        
        date_start_str = request.POST['date_start']
        date_end_str = request.POST['date_end']        
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d')
        
        # Actualizar los campos de la reserva
        booking.date_start = date_start
        booking.date_end = date_end
        booking.price = request.POST['totalValue']
        booking.customer_id = request.POST['customer']
        booking.save()
        
        # Guardar las nuevas cabañas asociadas a la reserva
        cabin_Id = request.POST.getlist('cabinId[]')
        cabin_price = request.POST.getlist('cabinPrice[]')

        for i in range(len(cabin_Id)):            
            cabin = Cabin.objects.get(pk=int(cabin_Id[i]))
            booking_cabin = Booking_cabin.objects.create(
                booking=booking,
                cabin=cabin,
                price=cabin_price[i]
            )
            booking_cabin.save()
        
        # Guardar los nuevos servicios asociados a la reserva
        service_Id = request.POST.getlist('serviceId[]')
        service_price = request.POST.getlist('servicePrice[]')
        
        for i in range(len(service_Id)):
            service = Service.objects.get(pk=int(service_Id[i]))
            booking_service = Booking_service.objects.create(
                booking=booking,
                service=service,
                price=service_price[i]
            )
            booking_service.save()
        
        messages.success(request, 'Reserva editada con éxito.')
        return redirect('booking')
    
    return render(request, 'booking/edit.html', {'booking': booking, 'customer_list': customer_list, 'cabin_list': cabin_list, 'service_list': service_list, 'booking_cabin': booking_cabin, 'booking_service': booking_service})

from django.shortcuts import get_object_or_404

@login_required
@user_passes_test(admin_or_staff)
def finish_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.status = 'Finalizada'
    booking.save()
    messages.success(request, 'Reserva finalizada con éxito.')
    return redirect('booking')

@login_required
@user_passes_test(admin_or_staff)
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelada'
    booking.save()
    return redirect('index')


@login_required
@user_passes_test(admin_or_staff)
def payment_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    total_payments = Payment.objects.filter(booking_id=booking_id).aggregate(total=models.Sum('amount'))
    if total_payments['total'] is not None:
        total_payments = total_payments['total']
    else:
        total_payments = 0    
    if request.method == 'POST':
        date = datetime.now().date()
        amount = request.POST['amount']
        payment_method = request.POST['payment_method']
        payment_booking = request.POST['payment_booking']
        payment = Payment.objects.create(
            date=date,
            amount=int(amount),
            payment_method=payment_method,
            booking=booking,
            status='Confirmado'
        )
        try:
            payment.save()     
            total_p = Payment.objects.filter(booking_id=booking_id).aggregate(total=models.Sum('amount'))       
            if  int(total_p['total']) >= (booking.price / 2) and int(total_p['total']) < booking.price:
                booking.status = 'Confirmada'
            elif int(total_p['total']) >= booking.price:
                booking.status = 'En ejecución'        
            booking.save()
            messages.success(request, 'Pago realizado correctamente.')
            return redirect('booking') 
        
        except:
            messages.error(request, 'Ocurrió un error al editar el Pago.')
            return redirect('booking')         
    return render(request, 'booking/payment_booking.html', {'booking': booking, 'total_payments': total_payments})

class ReportInvoicePdfView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking_cabin = Booking_cabin.objects.filter(booking=booking)
        booking_service = Booking_service.objects.filter(booking=booking)
        customer_list = Customer.objects.all()
        cabin_list = Cabin.objects.all()
        service_list = Service.objects.all()
        booking_cabin = Booking_cabin.objects.filter(booking_id=booking_id)
        booking_service = Booking_service.objects.filter(booking_id=booking_id)
        template = get_template('payment/invoice.html')
        context = {'booking': booking, 'customer_list': customer_list, 'cabin_list': cabin_list, 'service_list': service_list, 'booking_cabin': booking_cabin, 'booking_service': booking_service}
        html = template.render(context, request)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(html, dest=response)
        if pisaStatus.err:
            return HttpResponse('Hay un error al generar el PDF')
        return response 
    

from django.db.models import Q

@login_required
def booking(request):
    query = request.GET.get('q')
    if query:
        booking_list = Booking.objects.filter(
            Q(customer__name__icontains=query) | 
            Q(customer__document__icontains=query) |
            Q(date_booking__icontains=query) |
            Q(date_start__icontains=query) |
            Q(date_end__icontains=query) |
            Q(price__icontains=query) |
            Q(status__icontains=query)
        ).distinct()
    else:
        booking_list = Booking.objects.all()

    return render(request, 'booking/index.html', {'booking_list': booking_list})


