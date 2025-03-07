# residences/urls.py
from django.urls import path
from . import views

app_name = 'residences'

urlpatterns = [
    path('', views.residence_list, name='residence_list'),
    path('create/', views.residence_create, name='residence_create'),
    path('<int:id>/', views.residence_detail, name='residence_detail'),
    path('<int:id>/edit/', views.residence_edit, name='residence_edit'),
    path('<int:id>/delete/', views.residence_delete, name='residence_delete'),

    # Rutas para BlockName
    path('blocknames/', views.blockname_list, name='blockname_list'),
    path('blocknames/create/', views.blockname_create, name='blockname_create'),
    path('blocknames/<int:id>/edit/', views.blockname_edit, name='blockname_edit'),
    path('blocknames/<int:id>/delete/', views.blockname_delete, name='blockname_delete'),
]