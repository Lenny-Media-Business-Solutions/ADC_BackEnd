from rest_framework import viewsets, permissions
from .models import Gallery
from .serializers import GallerySerializer
from users.permissions import IsActivePortalStaff

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsActivePortalStaff()]
