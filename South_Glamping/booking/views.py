from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from customer.models import Customer
from cabin.models import Cabin
from service.models import Service
from booking.models import Booking
from booking_cabin.models import Booking_cabin
from booking_service.models import Booking_service
from payment.models import Payment
from django.db import models

def booking(request):    
    booking_list = Booking.objects.all()    
    return render(request, 'booking/index.html', {'booking_list': booking_list})

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
            price=request.POST['totalValue'],
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

def detail_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking_cabin = Booking_cabin.objects.filter(booking=booking)
    booking_service = Booking_service.objects.filter(booking=booking)
    payment = Payment.objects.filter(booking=booking)
    return render(request, 'booking/detail.html', {'booking': booking, 'booking_cabin': booking_cabin, 'booking_service': booking_service, 'payment': payment})


def change_status_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking.status = not booking.status
    booking.save()
    return redirect('booking')


def delete_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    try:
        booking.delete()        
        messages.success(request, 'Reserva eliminada correctamente.')
    except:
        messages.error(request, 'No se puede eliminar la reserva porque está asociada a un servicio.')
    return redirect('booking')

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking_cabin = Booking_cabin.objects.filter(booking=booking)
    booking_service = Booking_service.objects.filter(booking=booking)
    customer_list = Customer.objects.all()
    cabin_list = Cabin.objects.all()
    service_list = Service.objects.all()
    booking_cabin = Booking_cabin.objects.filter(booking_id=booking_id)
    print(booking_cabin)
    booking_service = Booking_service.objects.filter(booking_id=booking_id)
    
    
    if request.method == 'POST':
        date_start_str = request.POST['date_start']
        date_end_str = request.POST['date_end']        
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d')
        
        
        # Actualizar los campos de la reserva
        booking.date_start = date_start
        booking.date_end = date_end
        booking.price = request.POST['totalValue']
        booking.customer_id=request.POST['customer']
        booking.save()
        
        # Actualizar las cabañas asociadas a la reserva
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
        
        # Actualizar los servicios asociados a la reserva
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
            return redirect('bookings') 
        
        except Exception as e:
            return redirect('booking')         
    return render(request, 'booking/payment_booking.html', {'booking': booking, 'total_payments': total_payments})
