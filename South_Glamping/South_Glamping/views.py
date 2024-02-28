from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from South_Glamping.forms import RegisterForm
from customer.models import Customer
from django.contrib.auth.models import Group

def index(request):
    return render(request, 'index.html')



def landingpage(request):
        return render(request,'landingpage.html')

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            return render(request, 'index.html', {'user': authenticated_user})
        else:
            error = 'Usuario o contraseña incorrectos.'
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