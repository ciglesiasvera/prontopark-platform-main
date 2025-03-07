from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='list'),
    path('create/', views.create_alert, name='create'),
    path('<int:alert_id>/', views.alert_detail, name='detail'),
    path('<int:alert_id>/resolve/', views.resolve_alert, name='resolve'),
    path('<int:alert_id>/dismiss/', views.dismiss_alert, name='dismiss'),
]
