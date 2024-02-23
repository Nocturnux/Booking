from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from customer.models import Customer
from cabin.models import Cabin
from service.models import Service
from booking.models import Booking
from booking_cabin.models import Booking_cabin
from booking_service.models import Booking_service
from payment.models import Payment

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
            status='Por confirmar',
            customer_id=request.POST['customer']
        )
        booking.save()        
        cabin_Id = request.POST.getlist('cabinId[]')
        cabin_price = request.POST.getlist('cabinPrice[]')
        service_Id = request.POST.getlist('serviceId[]')
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
    booking = Booking.objects.get(pk=booking_id)
    try:
       booking.save()
       messages.success(request, 'Cabaña actualizada correctamente.')
    except:
        messages.error(request, 'Ocurrió un error al editar la cabaña.')
        return redirect('booking')    
    return render(request, 'booking/edit.html', {'form': form})

