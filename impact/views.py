from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ImpactStory
from .serializers import ImpactStorySerializer

class ImpactStoryViewSet(viewsets.ModelViewSet):
    queryset = ImpactStory.objects.all()
    serializer_class = ImpactStorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = ImpactStory.objects.all()
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        return queryset
