from rest_framework import serializers
from .models import Project
from programs.serializers import ProgramSerializer

class ProjectSerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
