from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from .models import Report
from .forms import ReportForm
from .decorators import role_required
from reservations.models import Reservation
from residences.models import Residence
from parkings.models import Parking

@login_required
def report_list(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports/report_list.html', {
        'reports': reports
    })

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge', 'parking_owner', 'resident'])
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, _('Report created successfully'))
            return redirect('reports:list')
    else:
        form = ReportForm()

    return render(request, 'reports/create_report.html', {
        'form': form
    })

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    return render(request, 'reports/report_detail.html', {
        'report': report
    })

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def parking_report(request):
    # Filtrar reservas por rango de fechas, usuario, lote y bloque
    reservations = Reservation.objects.filter(
        start_datetime__gte=request.GET.get('start_date'),
        end_datetime__lte=request.GET.get('end_date')
    )

    # Agrupar por lote y bloque
    parking_report = reservations.values('parking__lot__name', 'parking__block_name').annotate(total_reservations=Count('id'))

    return render(request, 'reports/parking_report.html', {
        'parking_report': parking_report
    })

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def residence_report(request):
    # Filtrar residencias por nombre de bloque y propietario
    residences = Residence.objects.filter(
        block_name__name=request.GET.get('block_name'),
        owner__username=request.GET.get('owner')
    )

    return render(request, 'reports/residence_report.html', {
        'residences': residences
    })
