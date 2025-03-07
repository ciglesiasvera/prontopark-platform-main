from django.contrib import admin
from .models import Lot, Parking

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('number', 'lot', 'owner', 'visit_parking')
    list_filter = ('visit_parking', 'owner__role')
    search_fields = ('number', 'owner__username', 'lot__name')
    raw_id_fields = ('owner', 'lot')
    ordering = ('lot', 'number')
