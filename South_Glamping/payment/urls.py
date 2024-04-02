from . import views
from django.urls import path
from .views import ReportInvoicePdfView

urlpatterns = [      
    path('', views.payment, name='payment'),
    path('create/', views.create_payment, name='create_payment'),    
    path('detail/<int:payment_id>/', views.detail_payment, name='detail_payment'),
    path('edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('invoice/<int:payment_id>/', ReportInvoicePdfView.as_view(), name='payment_invoice_pdf')
]