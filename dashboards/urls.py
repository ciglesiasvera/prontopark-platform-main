from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
path('supervisor/', views.supervisor_dashboard, name='supervisor'),
path('admin/', views.admin_dashboard, name='admin'),
path('concierge/', views.concierge_dashboard, name='concierge'),
path('parking_owner/', views.parking_owner_dashboard, name='parking_owner'),
path('resident/', views.resident_dashboard, name='resident'),
path('visit/', views.visit_dashboard, name='visit'),
]
