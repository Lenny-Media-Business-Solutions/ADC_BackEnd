from rest_framework import viewsets, permissions
from .models import VolunteerApplication
from .serializers import VolunteerApplicationSerializer
from users.permissions import IsActivePortalStaff

class VolunteerApplicationViewSet(viewsets.ModelViewSet):
    queryset = VolunteerApplication.objects.all()
    serializer_class = VolunteerApplicationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsActivePortalStaff()]

    def perform_create(self, serializer):
        from core.utils import send_submission_notification
        instance = serializer.save()
        send_submission_notification('volunteer application', serializer.data)
