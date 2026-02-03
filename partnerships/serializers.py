from rest_framework import serializers
from .models import PartnershipInquiry
from programs.serializers import ProgramSerializer

class PartnershipInquirySerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)

    class Meta:
        model = PartnershipInquiry
        fields = '__all__'
        read_only_fields = ('status', 'created_at')
