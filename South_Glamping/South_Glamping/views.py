from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from South_Glamping.forms import RegisterForm
from customer.models import Customer
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from service.models import Service
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from booking.models import Booking 
from babel.dates import format_date
import json
from datetime import date
from django.db.models import Sum
import calendar
from collections import Counter
from cabin.models import Cabin
from booking_cabin.models import Booking_cabin
from cabin_type.models import Cabin_type  
from booking_service.models import Booking_service 
from django.contrib.auth.decorators import login_required  


def get_booking_data():
    data = []
    for month in range(1, 7):
        bookings = Booking.objects.filter(date_start__month=month).count()
        data.append(bookings)
    return data


def get_profit_data():
    data = []
    for month in range(1, 7):  
        bookings = Booking.objects.filter(date_booking__month=month)
        monthly_profit = bookings.aggregate(total_profit=Sum('price'))['total_profit'] or 0
        data.append(monthly_profit)
    return data

def get_typecabin_data():
    cabin_types = [cabin_type.name for cabin_type in Cabin_type.objects.all()]
    cabin_data = []
    for cabin_type in cabin_types:
        cabins = Cabin.objects.filter(cabin_type__name=cabin_type)
        bookings = Booking_cabin.objects.filter(cabin__cabin_type__name=cabin_type)
        cabin_data.append(bookings.count())
    return cabin_types, cabin_data

def get_service_data():
    service_names = [service.name for service in Service.objects.all()]
    service_data = []
    for service_name in service_names:
        bookings = Booking_service.objects.filter(service__name=service_name)
        service_data.append(bookings.count())
    return service_names, service_data

def get_admin_data():
    # Obtén los datos que necesitas para el administrador
    months = [format_date(date(month=i, day=1, year=2024), 'MMMM', locale='es_ES') for i in range(1,7 )]
    booking_data = get_booking_data()
    profit_data = get_profit_data()
    cabin_types, cabin_data = get_typecabin_data()
    service_names, service_data = get_service_data()  
    

    return months, booking_data, profit_data, cabin_data, cabin_types, service_names, service_data

@login_required
def index(request):
    services = Service.objects.filter(status=True)
    cabin_types = Cabin_type.objects.filter(status=True)
    cabins = Cabin.objects.filter(status=True)


    if request.user.is_superuser:  # Si el usuario es un administrador
        months, booking_data, profit_data, cabin_data, cabin_types, service_names, service_data = get_admin_data()  # Asume que esta función obtiene los datos del administrador

        context = {
            'months': json.dumps(months),
            'data': json.dumps(booking_data),
            'profit': json.dumps(profit_data),
            'cabin_data': json.dumps(cabin_data),
            'cabin_types': json.dumps(cabin_types),
            'service_names': json.dumps(service_names),
            'service_data': json.dumps(service_data),
            'services': services,
            'cabin_types': cabin_types,
            'cabins': cabins,
            'request': request
        }
        
        return render(request, 'index.html', context)  

    else:  # Si el usuario no es un administrador
        return render(request, 'index.html', {'services': services, 'cabin_types': cabin_types, 'cabins': cabins, 'request': request })


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def landingpage(request):
    services = Service.objects.filter(status=True)
    cabin_types = Cabin_type.objects.filter(status=True)
    cabins = Cabin.objects.filter(status=True)
    return render(request, 'landingpage.html', {'services': services, 'cabin_types': cabin_types, 'cabins': cabins})
        

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            return redirect( 'index')
        else:
            error = '¡Usuario o contraseña incorrectos!'
            return render(request, 'login.html', {'error': error})    
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)    
    return redirect('login')

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            document = form.cleaned_data['document']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            cellphone = form.cleaned_data['cellphone']
            username = email
            user = User.objects.create_user(username, email, password, first_name=name, last_name=last_name)
            user.save()
            group = Group.objects.get(name='clientes')
            user.groups.add(group)
        if user is not None:            
            client = Customer.objects.filter(document=document).first()
            if client is None:
                name = form.cleaned_data['name'] + ' ' + form.cleaned_data['last_name']
                client = Customer(None, name, document=document, email=email, cellphone=cellphone)
                client.save()
                return redirect('login')               
        return redirect('login')     
    return render(request, 'register.html', {'form': form})

def generate_password():
    characters = string.ascii_letters + string.digits
    length = 10
    return ''.join(random.choice(characters) for i in range(length))

def send_email(addressee, password):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender = 'southglamping.sg@gmail.com'
    password_smtp = 'cwne kdqi pzpn xoln'

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = sender #remitente
    message['to'] = addressee #destinatario
    message['Subject'] = 'Recuperación de contraseña'

    body = body = f"""Hola.  
    
Tu nueva contraseña para acceder a South Glamping es: {password}. Por favor, no olvides cambiar esta contraseña en tu próximo inicio de sesión.

Saludos,
South Glamping."""
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # Iniciar sesión en el servidor SMTP
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender, password_smtp)

    # Enviar el correo electrónico
    server.send_message(message)

    # Cerrar la conexión
    server.quit()

# Función principal
def recuperar_contraseña (email):
    destination_email= email
    new_password= generate_password()
    send_email(destination_email, new_password)

def recover_password(request):
    message = None
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            recuperar_contraseña(email)
            # Consultar usuario por email y cambiar la contraseña
            message = f"Se ha enviado un correo a: {email}, con la nueva contraseña."
        except User.DoesNotExist:
            message = "¡El correo ingresado no está registrado!"
        
    return render(request, 'recover_password.html', {'message': message})
            











