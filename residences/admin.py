from django.contrib import admin
from .models import BlockName, Residence, User

@admin.register(BlockName)
class BlockNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Residence)
class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('number', 'block_name', 'owner', 'created_at')
    list_filter = ('block_name', 'owner__role')
    search_fields = ('number', 'owner__username')
    raw_id_fields = ('owner',)
    ordering = ('block_name', 'number')