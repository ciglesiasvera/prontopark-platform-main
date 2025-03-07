from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('parking', 'user', 'status', 'created_at')
    list_filter = ('status', 'parking__lot__name')
    search_fields = ('user__username', 'parking__number')
    ordering = ('-created_at',)
