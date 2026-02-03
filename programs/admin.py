from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)
