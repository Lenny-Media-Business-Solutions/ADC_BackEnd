from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ImpactStory
from .serializers import ImpactStorySerializer
from users.permissions import IsActivePortalStaff

class ImpactStoryViewSet(viewsets.ModelViewSet):
    queryset = ImpactStory.objects.all()
    serializer_class = ImpactStorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsActivePortalStaff()]

    def get_queryset(self):
        queryset = ImpactStory.objects.all()
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        return queryset
