from django.urls import path
from .views import (
    # ... tus vistas de registro, login, etc.
    register_resident,
    register_parking_owner,
    register_concierge,
    register_admin,
    user_login,
    user_logout,
    user_profile,
    user_list,
)

app_name = 'users'

urlpatterns = [
    # Rutas de registro, login, etc.
    path('register/resident/', register_resident, name='register_resident'),
    path('register/parking_owner/', register_parking_owner, name='register_parking_owner'),
    path('register/concierge/', register_concierge, name='register_concierge'),
    path('register/admin/', register_admin, name='register_admin'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('', user_list, name='user_list'),
]
