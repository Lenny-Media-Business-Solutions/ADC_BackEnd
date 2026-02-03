from django.contrib import admin
from .models import PartnershipInquiry

@admin.register(PartnershipInquiry)
class PartnershipInquiryAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'program', 'partnership_type', 'status', 'created_at')
    list_filter = ('status', 'partnership_type', 'program')
    search_fields = ('organization_name', 'contact_person', 'email')
