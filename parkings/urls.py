from django.urls import path
from . import views

app_name = 'parkings'

urlpatterns = [
    path('', views.parking_list, name='parking_list'),
    path('<int:id>/', views.parking_detail, name='parking_detail'),
    path('create/', views.parking_create, name='parking_create'),
    path('edit/<int:id>/', views.parking_edit, name='parking_edit'),
    path('delete/<int:id>/', views.parking_delete, name='parking_delete'),
    path('lots/', views.lot_list, name='lot_list'),
    path('lots/create/', views.lot_create, name='lot_create'),
    path('lots/edit/<int:id>/', views.lot_edit, name='lot_edit'),
    path('lots/delete/<int:id>/', views.lot_delete, name='lot_delete'),
]
