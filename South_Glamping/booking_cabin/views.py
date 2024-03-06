from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required

from booking_cabin.models import Booking_cabin


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(admin_or_staff)
def booking_cabin(request):    
    booking_cabin_list = Booking_cabin.objects.all()    
    return render(request, 'booking_cabin/index.html', {'booking_cabin_list': booking_cabin_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_booking_cabin(request,booking_cabin_id):
    booking_cabin = Booking_cabin.objects.get(pk=booking_cabin_id)
    booking_cabin.save()
    return redirect('booking_cabin')
