
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomerForm
from customer.models import Customer

from .forms import CustomerForm
from django.http import JsonResponse
from django.contrib import messages


def admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@login_required
@user_passes_test(admin_or_staff)
def customer(request):    
    customer_list = Customer.objects.all()    
    return render(request, 'customer/index.html', {'customer_list': customer_list})


@login_required
@user_passes_test(admin_or_staff)
def change_status_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    customer.status = not customer.status
    customer.save()
    return redirect('customer')


@login_required
@user_passes_test(admin_or_staff)
def create_customer(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al crear el cliente.')        
        return redirect('customer')    
    return render(request, 'customer/create.html', {'form': form})


@login_required
@user_passes_test(admin_or_staff)
def detail_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    data = { 'name': customer.name, 'document': customer.document, 'cellphone': customer.cellphone, 'status': customer.status }    
    return JsonResponse(data)


@login_required
@user_passes_test(admin_or_staff)
def delete_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    try:
        customer.delete()        
        messages.success(request, 'Cliente eliminado correctamente.')
    except:
        messages.error(request, 'No se puede eliminar el cliente porque está asociado a una reserva')
    return redirect('customer')


@login_required
@user_passes_test(admin_or_staff)
def edit_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar el cliente.')        
        return redirect('customer')    
    return render(request, 'customer/editar.html', {'form': form})