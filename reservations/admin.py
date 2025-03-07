from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('parking', 'user', 'start_datetime', 'end_datetime', 'status')
    list_filter = ('status', 'parking__lot__name')
    search_fields = ('user__username', 'parking__number')
    ordering = ('-start_datetime',)
