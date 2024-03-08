"""
URL configuration for South_Glamping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingpage, name="landingpage"),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('customer/', include('customer.urls')),
    path('service/', include('service.urls')),
    path('booking/', include('booking.urls')),  
    path('cabin_type/', include('cabin_type.urls')),
    path('payment/', include('payment.urls')), 
    path('cabin/', include('cabin.urls')),  
    path('booking_service/', include('booking_service.urls')),
    path('booking_cabin/', include('booking_cabin.urls')),
    path('recover',views.recover, name='recover')
]
