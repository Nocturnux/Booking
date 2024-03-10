from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from cabin.models import Cabin
from django.http import JsonResponse
from django.contrib import messages
from .forms import CabinForm


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(admin_or_staff)
def cabin(request):    
    cabin_list = Cabin.objects.all()    
    return render(request, 'cabin/index.html', {'cabin_list': cabin_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_cabin(request, cabin_id):
    cabin = Cabin.objects.get(pk=cabin_id)
    cabin.status = not cabin.status
    cabin.save()
    return redirect('cabin')


@login_required
@user_passes_test(admin_or_staff)
def create_cabin(request):
    form = CabinForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Cabaña creada correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al crear la cabaña.')        
        return redirect('cabin')    
    return render(request, 'cabin/create.html', {'form': form})

@login_required
@user_passes_test(admin_or_staff)
def detail_cabin(request, cabin_id):
    cabin = Cabin.objects.get(pk=cabin_id)
    data = { 'name': cabin.name, 'image': cabin.image.url, 'capacity': cabin.capacity, 'cabin_type': str(cabin.cabin_type), 'description': cabin.description,'price': cabin.price, } 
    return JsonResponse(data)


@login_required
@user_passes_test(admin_or_staff)
def delete_cabin(request, cabin_id):
    cabin = Cabin.objects.get(pk=cabin_id)
    try:
        cabin.delete()        
        messages.success(request, 'Cabaña eliminada correctamente.')
    except:
        messages.error(request, 'No se puede eliminar la cabaña.')
    return redirect('cabin')

@login_required
@user_passes_test(admin_or_staff)
def edit_cabin(request, cabin_id):
    cabin = Cabin.objects.get(pk=cabin_id)
    form = CabinForm(request.POST or None, request.FILES or None, instance=cabin)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Cabaña actualizada correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar la cabaña.')
        return redirect('cabin')    
    return render(request, 'cabin/edit.html', {'form': form})

