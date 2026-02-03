from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    # We still keep slug as the default for auto-generated URLs if any
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Try finding by Slug first, then by ID
        try:
            return queryset.get(slug=lookup_value)
        except News.DoesNotExist:
            try:
                return queryset.get(id=lookup_value)
            except (News.DoesNotExist, ValueError):
                raise Http404

    def get_queryset(self):
        # Only show drafts if explicitly requested via query param (e.g. for Admin Dashboard)
        # Or if it's a detail action (accessing a specific object) by an authenticated user
        include_drafts = self.request.query_params.get('include_drafts', 'false').lower() == 'true'
        is_detail = self.detail or 'update_status' in self.request.path or 'toggle_status' in self.request.path
        
        if (include_drafts or is_detail) and self.request.user.is_authenticated:
            return News.objects.all()
        return News.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, slug=None):
        news = self.get_object()
        news.is_published = not news.is_published
        news.save()
        return Response({
            'status': 'success',
            'is_published': news.is_published,
            'message': f"News is now {'published' if news.is_published else 'unpublished'}"
        })

    @action(detail=True, methods=['post'])
    def update_status(self, request, slug=None):
        news = self.get_object()
        is_published = request.data.get('is_published')
        if is_published is None:
            return Response({'error': 'is_published field is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        news.is_published = bool(is_published)
        news.save()
        return Response({
            'status': 'success',
            'is_published': news.is_published,
            'message': f"News status updated to {'published' if news.is_published else 'unpublished'}"
        })
