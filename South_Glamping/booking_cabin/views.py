from django.shortcuts import render
from django.shortcuts import render, redirect

from booking_cabin.models import Booking_cabin

def booking_cabin(request):    
    booking_cabin_list = Booking_cabin.objects.all()    
    return render(request, 'booking_cabin/index.html', {'booking_cabin_list': booking_cabin_list})

def change_status_booking_cabin(request,booking_cabin_id):
    booking_cabin = Booking_cabin.objects.get(pk=booking_cabin_id)
    booking_cabin.save()
    return redirect('booking_cabin')
