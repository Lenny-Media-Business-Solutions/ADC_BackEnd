from rest_framework import serializers
from .models import VolunteerApplication

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = '__all__'
        read_only_fields = ('status', 'created_at')
