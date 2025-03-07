from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    ResidentRegistrationForm,
    ParkingOwnerRegistrationForm,
    ConciergeRegistrationForm,
    AdminRegistrationForm,
)
from .decorators import role_required
from .models import User
from reservations.models import Reservation, ReservationStatus

# Mapeo de rol → nombre de la URL (dashboard)
ROLE_LOGIN_MAP = {
    "supervisor": "dashboards:supervisor",
    "admin": "dashboards:admin",
    "concierge": "dashboards:concierge",
    "parking_owner": "dashboards:parking_owner",
    "resident": "dashboards:resident",
    "visit": "dashboards:visit",  # O redirige a una vista/URL genérica
}


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # Redirige según el rol del usuario
            return redirect(ROLE_LOGIN_MAP.get(user.role, "visit_dashboard"))
        else:
            messages.error(request, "Credenciales inválidas o cuenta inactiva")
            return render(request, "users/login.html")
    return render(request, "users/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("users:login")


@login_required
def user_profile(request):
    return render(request, "users/user_profile.html")


@login_required
@role_required(roles=["supervisor", "admin"])
def register_resident(request):
    if request.method == "POST":
        form = ResidentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registro exitoso. El residente puede iniciar sesión ahora."
            )
            return redirect("users:login")
    else:
        form = ResidentRegistrationForm()
    return render(request, "users/register_resident.html", {"form": form})


@login_required
@role_required(roles=["supervisor", "admin"])
def register_parking_owner(request):
    if request.method == "POST":
        form = ParkingOwnerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Registro exitoso. El propietario de estacionamiento puede iniciar sesión ahora.",
            )
            return redirect("users:login")
    else:
        form = ParkingOwnerRegistrationForm()
    return render(request, "users/register_parking_owner.html", {"form": form})


@login_required
@role_required(roles=["supervisor", "admin"])
def register_concierge(request):
    if request.method == "POST":
        form = ConciergeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registro exitoso. El conserje puede iniciar sesión ahora."
            )
            return redirect("users:login")
    else:
        form = ConciergeRegistrationForm()
    return render(request, "users/register_concierge.html", {"form": form})


@login_required
@role_required(roles=["supervisor"])
def register_admin(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Registro exitoso. El administrador puede iniciar sesión ahora.",
            )
            return redirect("users:login")
    else:
        form = AdminRegistrationForm()
    return render(request, "users/register_admin.html", {"form": form})


@login_required
@role_required(roles=["supervisor", "admin"])
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})