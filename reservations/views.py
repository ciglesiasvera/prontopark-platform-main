from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Reservation, ReservationStatus
from .forms import ReservationForm
from parkings.models import Parking
from .decorators import role_required
from django.db.models import Q


@login_required
def reservation_list(request):
    if request.user.role == "supervisor" or request.user.role == "admin":
        reservations = Reservation.objects.all()
    elif request.user.role == "parking_owner":
        reservations = Reservation.objects.filter(
            Q(parking__owner=request.user) | Q(user=request.user)
        )
    elif request.user.role == "resident":
        reservations = Reservation.objects.filter(user=request.user)
    elif request.user.role == "concierge":
        reservations = Reservation.objects.filter(parking__visit_parking=True)

    return render(
        request, "reservations/reservation_list.html", {"reservations": reservations}
    )


@login_required
@role_required(roles=["supervisor", "admin", "parking_owner", "resident", "concierge"])
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.status = ReservationStatus.PENDING
            reservation.save()
            messages.success(request, _("Reserva creada con éxito."))
            return redirect("reservations:list")
    else:
        form = ReservationForm()

    return render(
        request,
        "reservations/create_reservation.html",
        {"form": form},
    )


@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(
        request, "reservations/reservation_detail.html", {"reservation": reservation}
    )


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        if reservation.status in [
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED,
        ]:
            reservation.status = ReservationStatus.CANCELLED
            reservation.save()
            messages.success(request, _("Reserva cancelada exitosamente."))
        else:
            messages.error(request, _("Esta reserva no pudo ser cancelada."))
        return redirect("reservations:list")
    return render(
        request, "reservations/cancel_reservation.html", {"reservation": reservation}
    )


def check_parking_availability(request):
    if request.method == "GET":
        parking_id = request.GET.get("parking_id")
        start_datetime = request.GET.get("start_datetime")
        end_datetime = request.GET.get("end_datetime")

        overlapping_reservations = Reservation.objects.filter(
            parking_id=parking_id,
            status__in=[ReservationStatus.PENDING, ReservationStatus.CONFIRMED],
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime,
        )

        is_available = not overlapping_reservations.exists()

        return render(
            request,
            "reservations/availability_check.html",
            {"is_available": is_available},
        )


@login_required
@role_required(roles=["parking_owner"])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user == reservation.parking.owner:
        reservation.status = ReservationStatus.CONFIRMED
        reservation.save()
        messages.success(request, _("Reservation approved successfully"))
    else:
        messages.error(
            request, _("You do not have permission to approve this reservation")
        )
    return redirect("reservations:list")


@login_required
@role_required(roles=["parking_owner"])
def reject_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user == reservation.parking.owner:
        reservation.status = ReservationStatus.CANCELLED
        reservation.save()
        messages.success(request, _("Reservation rejected successfully"))
    else:
        messages.error(
            request, _("You do not have permission to reject this reservation")
        )
    return redirect("reservations:list")


@login_required
@role_required(roles=["supervisor", "admin", "concierge"])
def approve_visit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.parking.visit_parking:
        reservation.status = ReservationStatus.CONFIRMED
        reservation.save()
        messages.success(request, _("Reservation approved successfully"))
    else:
        messages.error(
            request, _("You do not have permission to approve this reservation")
        )
    return redirect("reservations:list")


@login_required
@role_required(roles=["supervisor", "admin", "concierge"])
def reject_visit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.parking.visit_parking:
        reservation.status = ReservationStatus.CANCELLED
        reservation.save()
        messages.success(request, _("Reservation rejected successfully"))
    else:
        messages.error(
            request, _("You do not have permission to reject this reservation")
        )
    return redirect("reservations:list")
