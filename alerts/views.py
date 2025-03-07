from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Alert, AlertStatus
from .forms import AlertForm
from .decorators import role_required

@login_required
def alert_list(request):
    alerts = Alert.objects.all()
    #alerts = Alert.objects.filter(user=request.user)
    return render(request, 'alerts/alert_list.html', {
        'alerts': alerts
    })

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge', 'parking_owner', 'resident'])
def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.status = AlertStatus.PENDING
            alert.save()
            messages.success(request, _('Alert created successfully'))
            return redirect('alerts:list')
    else:
        form = AlertForm()

    return render(request, 'alerts/create_alert.html', {
        'form': form
    })

@login_required
def alert_detail(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    return render(request, 'alerts/alert_detail.html', {
        'alert': alert
    })

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def resolve_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    if request.user.role in ['supervisor', 'admin', 'concierge']:
        alert.status = AlertStatus.RESOLVED
        alert.save()
        messages.success(request, _('Alert resolved successfully'))
    else:
        messages.error(request, _('You do not have permission to resolve this alert'))
    return redirect('alerts:list')

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def dismiss_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    if request.user.role in ['supervisor', 'admin', 'concierge']:
        alert.status = AlertStatus.DISMISSED
        alert.save()
        messages.success(request, _('Alert dismissed successfully'))
    else:
        messages.error(request, _('You do not have permission to dismiss this alert'))
    return redirect('alerts:list')
