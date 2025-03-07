from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_type', 'created_at')
    list_filter = ('report_type',)
    search_fields = ('user__username',)
    ordering = ('-created_at',)

