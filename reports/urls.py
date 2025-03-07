from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='list'),
    path('create/', views.create_report, name='create'),
    path('<int:report_id>/', views.report_detail, name='detail'),
    path('parking_report/', views.parking_report, name='parking_report'),
    path('residence_report/', views.residence_report, name='residence_report'),
]
