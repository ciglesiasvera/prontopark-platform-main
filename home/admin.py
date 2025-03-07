from django.contrib import admin
from .models import HomePageContent

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    """
    Admin configuration for HomePageContent model
    """
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at')
