from . import views
from django.urls import path
from .views import ReportInvoicePdfView


urlpatterns = [      
    path('', views.booking, name='booking'),
    path('create/', views.create_booking, name='create_booking'),
    path('detail/<int:booking_id>/', views.detail_booking, name='detail_booking'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('payment_booking/<int:booking_id>/', views.payment_booking, name='payment_booking'),
    path('booking/finish/<int:booking_id>/', views.finish_booking, name='finish_booking'),
    path('invoice/<int:booking_id>/', ReportInvoicePdfView.as_view(), name='invoice')
]
