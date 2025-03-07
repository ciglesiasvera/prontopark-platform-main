from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='list'),
    path('create/', views.create_reservation, name='create'),
    path('<int:reservation_id>/', views.reservation_detail, name='detail'),
    path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel'),
    path('availability/', views.check_parking_availability, name='availability'),
    path('<int:reservation_id>/approve/', views.approve_reservation, name='approve'),
    path('<int:reservation_id>/reject/', views.reject_reservation, name='reject'),
    path('<int:reservation_id>/approve_visit/', views.approve_visit_reservation, name='approve_visit'),
    path('<int:reservation_id>/reject_visit/', views.reject_visit_reservation, name='reject_visit'),
]