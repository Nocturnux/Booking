from . import views
from django.urls import path

urlpatterns = [      
    path('', views.booking_service, name='booking_service'),   
    path('booking_service_status_/<int:booking_service_id>/', views.change_status_booking_service, name='booking_service_status'),         
]