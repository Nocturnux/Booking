from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from booking_service.models import Booking_service
from service.models import Service
from booking.models import Booking


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(admin_or_staff)
def booking_service(request):    
    booking_service_list = Booking_service.objects.all()    
    return render(request, 'booking_service/index.html', {'booking_service_list': booking_service_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_booking_service(request, booking_service_id):
    booking_service = Booking_service.objects.get(pk=booking_service_id)
    booking_service.save()
    return redirect('booking_service')
