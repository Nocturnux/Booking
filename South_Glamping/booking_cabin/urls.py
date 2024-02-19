from . import views
from django.urls import path

urlpatterns = [      
    path('', views.booking_cabin, name='booking_cabin'),
	path('booking_cabin_status_/<int:booking_cabin_id>/', views.change_status_booking_cabin, name='booking_cabin_status'),            
]