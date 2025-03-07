from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parking, Lot
from .forms import ParkingForm, LotForm
from users.decorators import role_required

# Vistas para Parking
def parking_list(request):
    parkings = Parking.objects.all()
    return render(request, 'parkings/parking_list.html', {'parkings': parkings})

def parking_detail(request, id):
    parking = get_object_or_404(Parking, id=id)
    return render(request, 'parkings/parking_detail.html', {'parking': parking})

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def parking_create(request):
    if request.method == 'POST':
        form = ParkingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estacionamiento creado exitosamente.')
            return redirect('parkings:parking_list')
    else:
        form = ParkingForm()
    return render(request, 'parkings/parking_create.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def parking_edit(request, id):
    parking = get_object_or_404(Parking, id=id)
    if request.method == 'POST':
        form = ParkingForm(request.POST, instance=parking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estacionamiento actualizado exitosamente.')
            return redirect('parkings:parking_list')
    else:
        form = ParkingForm(instance=parking)
    return render(request, 'parkings/parking_edit.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin', 'concierge'])
def parking_delete(request, id):
    parking = get_object_or_404(Parking, id=id)
    if request.method == 'POST':
        parking.delete()
        messages.success(request, 'Estacionamiento eliminado exitosamente.')
        return redirect('parkings:parking_list')
    return render(request, 'parkings/parking_delete.html', {'parking': parking})

# Vistas para Lot
def lot_list(request):
    lots = Lot.objects.all()
    return render(request, 'parkings/lot_list.html', {'lots': lots})

@login_required
@role_required(roles=['supervisor', 'admin'])
def lot_create(request):
    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote creado exitosamente.')
            return redirect('parkings:lot_list')
    else:
        form = LotForm()
    return render(request, 'parkings/lot_create.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def lot_edit(request, id):
    lot = get_object_or_404(Lot, id=id)
    if request.method == 'POST':
        form = LotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote actualizado exitosamente.')
            return redirect('parkings:lot_list')
    else:
        form = LotForm(instance=lot)
    return render(request, 'parkings/lot_edit.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def lot_delete(request, id):
    lot = get_object_or_404(Lot, id=id)
    if request.method == 'POST':
        lot.delete()
        messages.success(request, 'Lote eliminado exitosamente.')
        return redirect('parkings:lot_list')
    return render(request, 'parkings/lot_delete.html', {'lot': lot})
