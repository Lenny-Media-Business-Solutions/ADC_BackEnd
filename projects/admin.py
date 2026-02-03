from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'location', 'status', 'created_at')
    list_filter = ('program', 'status')
    search_fields = ('title', 'location')
