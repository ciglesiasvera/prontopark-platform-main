from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlockName, Residence
from .forms import BlockNameForm, ResidenceForm
from users.decorators import role_required

# Vistas para Residence
def residence_list(request):
    residences = Residence.objects.all()
    return render(request, 'residences/residence_list.html', {'residences': residences})

def residence_detail(request, id):
    residence = get_object_or_404(Residence, id=id)
    return render(request, 'residences/residence_detail.html', {'residence': residence})

@login_required
@role_required(roles=['supervisor', 'admin'])
def residence_create(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residencia creada exitosamente.')
            return redirect('residences:residence_list')
    else:
        form = ResidenceForm()
    return render(request, 'residences/residence_create.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def residence_edit(request, id):
    residence = get_object_or_404(Residence, id=id)
    if request.method == 'POST':
        form = ResidenceForm(request.POST, instance=residence)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residencia actualizada exitosamente.')
            return redirect('residences:residence_list')
    else:
        form = ResidenceForm(instance=residence)
    return render(request, 'residences/residence_edit.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def residence_delete(request, id):
    residence = get_object_or_404(Residence, id=id)
    if request.method == 'POST':
        residence.delete()
        messages.success(request, 'Residencia eliminada exitosamente.')
        return redirect('residences:residence_list')
    return render(request, 'residences/residence_delete.html', {'residence': residence})

# Vistas para BlockName
def blockname_list(request):
    blocknames = BlockName.objects.all()
    return render(request, 'residences/blockname_list.html', {'blocknames': blocknames})

@login_required
@role_required(roles=['supervisor', 'admin'])
def blockname_create(request):
    if request.method == 'POST':
        form = BlockNameForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nombre de bloque creado exitosamente.')
            return redirect('residences:blockname_list')
    else:
        form = BlockNameForm()
    return render(request, 'residences/blockname_create.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def blockname_edit(request, id):
    blockname = get_object_or_404(BlockName, id=id)
    if request.method == 'POST':
        form = BlockNameForm(request.POST, instance=blockname)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nombre de bloque actualizado exitosamente.')
            return redirect('residences:blockname_list')
    else:
        form = BlockNameForm(instance=blockname)
    return render(request, 'residences/blockname_edit.html', {'form': form})

@login_required
@role_required(roles=['supervisor', 'admin'])
def blockname_delete(request, id):
    blockname = get_object_or_404(BlockName, id=id)
    if request.method == 'POST':
        blockname.delete()
        messages.success(request, 'Nombre de bloque eliminado exitosamente.')
        return redirect('residences:blockname_list')
    return render(request, 'residences/blockname_delete.html', {'blockname': blockname})
