from . import views
from django.urls import path

urlpatterns = [      
    path('', views.cabin_type, name='cabin_type'),   
    path('cabin_type_status_/<int:cabin_type_id>/', views.change_status_cabin_type, name='cabin_type_status'),
    path('create/', views.create_cabin_type, name='create_cabin_type'), 
    path('detail/<int:cabin_type_id>/', views.detail_cabin_type, name='detail_cabin_type'),  
    path('delete/<int:cabin_type_id>/', views.delete_cabin_type, name='delete_cabin_type'),   
    path('edit/<int:cabin_type_id>/', views.edit_cabin_type, name='edit_cabin_type'),      
]