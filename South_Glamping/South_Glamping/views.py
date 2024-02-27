from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

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
    return redirect('landingpage')