from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PartnershipInquiry
from .serializers import PartnershipInquirySerializer

class PartnershipInquiryViewSet(viewsets.ModelViewSet):
    queryset = PartnershipInquiry.objects.all()
    serializer_class = PartnershipInquirySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        from core.utils import send_submission_notification
        instance = serializer.save()
        send_submission_notification('partnership', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        deleted_count, _ = PartnershipInquiry.objects.filter(id__in=ids).delete()
        return Response({'message': f'Successfully deleted {deleted_count} inquiries'}, status=status.HTTP_200_OK)
