from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from reservations.models import Reservation, ReservationStatus
from parkings.models import Parking


@login_required
@role_required(["supervisor", "admin", "concierge"])
def concierge_dashboard(request):
    pending_visit_reservations = Reservation.objects.filter(
        status=ReservationStatus.PENDING, parking__visit_parking=True
    )
    return render(
        request,
        "dashboards/concierge_dashboard.html",
        {"pending_visit_reservations": pending_visit_reservations},
    )


@login_required
@role_required(["supervisor", "admin", "parking_owner"])
def parking_owner_dashboard(request):
    pending_reservations = Reservation.objects.filter(
        status=ReservationStatus.PENDING, user=request.user
    )
    return render(
        request,
        "dashboards/parking_owner_dashboard.html",
        {"pending_reservations": pending_reservations},
    )


@login_required
@role_required(["supervisor", "admin", "resident"])
def resident_dashboard(request):
    return render(request, "dashboards/resident_dashboard.html")


@login_required
@role_required(["supervisor"])
def supervisor_dashboard(request):
    pending_visit_reservations = Reservation.objects.filter(
        status=ReservationStatus.PENDING, parking__visit_parking=True
    )
    return render(
        request,
        "dashboards/supervisor_dashboard.html",
        {"pending_visit_reservations": pending_visit_reservations},
    )


@login_required
@role_required(["supervisor", "admin"])
def admin_dashboard(request):
    pending_visit_reservations = Reservation.objects.filter(
        status=ReservationStatus.PENDING, parking__visit_parking=True
    )
    return render(
        request,
        "dashboards/admin_dashboard.html",
        {"pending_visit_reservations": pending_visit_reservations},
    )


def visit_dashboard(request):
    return render(request, "dashboards/visit_dashboard.html")
