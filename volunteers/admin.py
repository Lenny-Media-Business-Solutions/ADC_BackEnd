from django.contrib import admin
from .models import VolunteerApplication

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'area_of_interest', 'status', 'created_at')
    list_filter = ('status', 'area_of_interest')
    search_fields = ('full_name', 'email')
