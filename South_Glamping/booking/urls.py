from . import views
from django.urls import path


urlpatterns = [      
    path('', views.booking, name='booking'),
    path('create/', views.create_booking, name='create_booking'),
    path('detail/<int:booking_id>/', views.detail_booking, name='detail_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('payment_booking/<int:booking_id>/', views.payment_booking, name='payment_booking'),
    path('invoice/<int:booking_id>/', views.ReportInvoicePdfView.as_view(), name='ReportInvoicePdfView'),
]