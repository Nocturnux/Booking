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