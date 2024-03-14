from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import Cabin_typeForm
from cabin_type.models import Cabin_type
from django.http import JsonResponse
from django.contrib import messages


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(admin_or_staff)
def cabin_type(request):    
    cabin_type_list = Cabin_type.objects.all()    
    return render(request, 'cabin_type/index.html', {'cabin_type_list': cabin_type_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_cabin_type(request, cabin_type_id):
    cabin_type = Cabin_type.objects.get(pk=cabin_type_id)
    cabin_type.status = not cabin_type.status
    cabin_type.save()
    return redirect('cabin_type')



@login_required
@user_passes_test(admin_or_staff)
def create_cabin_type(request):
    form = Cabin_typeForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Tipo de cabaña creado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al crear el Tipo de cabaña.')        
        return redirect('cabin_type')    
    return render(request, 'cabin_type/create.html', {'form': form})



@login_required
@user_passes_test(admin_or_staff)
def detail_cabin_type(request, cabin_type_id):
    cabin_type = Cabin_type.objects.get(pk=cabin_type_id)
    data = { 'image':cabin_type.image.url, 'name': cabin_type.name, 'description':cabin_type.description,}    
    return JsonResponse(data)



@login_required
@user_passes_test(admin_or_staff)
def delete_cabin_type(request, cabin_type_id):
    cabin_type = Cabin_type.objects.get(pk=cabin_type_id)
    try:
        cabin_type.delete()        
        messages.success(request, 'Tipo de cabaña eliminado correctamente.')
    except:
        messages.error(request, 'No se puede eliminar el tipo de cabaña porque está asociado a una cabaña.')
    return redirect('cabin_type')



@login_required
@user_passes_test(admin_or_staff)
def edit_cabin_type(request, cabin_type_id):
    cabin_type = Cabin_type.objects.get(pk=cabin_type_id)
    form = Cabin_typeForm(request.POST or None, request.FILES or None, instance=cabin_type)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Tipo de cabaña actualizado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar el Tipo de cabaña.')        
        return redirect('cabin_type')    
    return render(request, 'cabin_type/edit.html', {'form': form})
