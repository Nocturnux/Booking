from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from service.models import Service
from .forms import ServiceForm
from django.http import JsonResponse
from django.contrib import messages


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(admin_or_staff)
def service(request):    
    service_list = Service.objects.all()    
    return render(request, 'service/index.html', {'service_list': service_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.status = not service.status
    service.save()
    return redirect('service')


@login_required
@user_passes_test(admin_or_staff)
def create_service(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Servicio creado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al crear el Servicio.')        
        return redirect('service')    
    return render(request, 'service/create.html', {'form': form})


@login_required
@user_passes_test(admin_or_staff)
def detail_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    data = {  'image': service.image.url, 'name': service.name, 'description': service.description, 'price': service.price, 'status': service.status }
    return JsonResponse(data)


@login_required
@user_passes_test(admin_or_staff)
def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    try:
        service.delete()        
        messages.success(request, 'Servicio eliminado correctamente.')
    except:
        messages.error(request, 'No se puede eliminar el servicio porque está asociada a una reserva.')
    return redirect('service')


@login_required
@user_passes_test(admin_or_staff)
def edit_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Servicio actualizado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar el Servicio.')        
        return redirect('service')    
    return render(request, 'service/edit.html', {'form': form})


def edit_reservation(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    rlodgings = Rlodging.objects.filter(reservation=reservation)
    rservices = Rservice.objects.filter(reservation=reservation)
    
    costumers_list = Costumer.objects.all()
    lodgings_list = Lodging.objects.all()
    services_list = Service.objects.all()    
    
    if request.method == 'POST':
        datess_str = request.POST['datess']
        dateff_str = request.POST['dateff']        
        datess = datetime.strptime(datess_str, '%Y-%m-%d')
        dateff = datetime.strptime(dateff_str, '%Y-%m-%d')

        # Actualizar los campos del objeto reservation con los valores recibidos del formulario
        reservation.datess = datess
        reservation.dateff = dateff
        reservation.price = request.POST['totalValue']
        reservation.costumer_id = request.POST['costumer']
        
        # Guardar los cambios en la base de datos      

        # Actualizar los objetos relacionales Rlodging y Rservice
        lodgings_Id = request.POST.getlist('lodgingId[]')
        lodgings_price = request.POST.getlist('lodgingPrice[]')
        services_Id = request.POST.getlist('serviceId[]')
        services_price = request.POST.getlist('servicePrice[]')       

        # Eliminar los objetos Rlodging y Rservice existentes asociados a esta reserva
        reservation.rlodging_set.all().delete()
        reservation.rservice_set.all().delete()

        # Crear nuevos objetos Rlodging y Rservice con los valores actualizados
        for i in range(len(lodgings_Id)):            
            lodging = Lodging.objects.get(pk=int(lodgings_Id[i]))
            rlodging = Rlodging.objects.create(
                reservation=reservation,
                lodging=lodging,
                price=lodgings_price[i]
            )
                
        for i in range(len(services_Id)):
            service = Service.objects.get(pk=int(services_Id[i]))
            rservice = Rservice.objects.create(
                reservation=reservation,
                service=service,
                price=services_price[i]
            )

            rservice.save()
            
        # Redireccionar a la página de listado de reservas con un mensaje de éxito
        messages.success(request, 'Reserva editada con éxito.')
        return redirect('reservations')
    
    # Si la solicitud es GET, renderizar el formulario de edición con los datos del objeto reservation
    return render(request, 'reservations/edit.html', {'reservation': reservation, 'costumers_list': costumers_list, 'lodgings_list': lodgings_list, 'services_list': services_list, 'rlodgings':rlodgings, 'rservices':rservices })