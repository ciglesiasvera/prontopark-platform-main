from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # URL para la página de inicio usando la vista basada en clase
    path('', views.HomePageView.as_view(), name='index'),
]
