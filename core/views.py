from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from programs.models import Program
from projects.models import Project
from volunteers.models import VolunteerApplication
from partnerships.models import PartnershipInquiry
from contact.models import ContactMessage
from impact.models import ImpactStory

class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Monthly Activity (Last 6 Months)
        six_months_ago = timezone.now() - timedelta(days=180)
        
        def get_monthly_totals(queryset):
            return queryset.filter(created_at__gte=six_months_ago) \
                .annotate(month=TruncMonth('created_at')) \
                .values('month') \
                .annotate(count=Count('id')) \
                .order_by('month')

        vol_counts = get_monthly_totals(VolunteerApplication.objects)
        msg_counts = get_monthly_totals(ContactMessage.objects)
        part_counts = get_monthly_totals(PartnershipInquiry.objects)

        # Combine results by month
        monthly_data = {}
        for item in vol_counts:
            m = item['month'].strftime('%b')
            monthly_data[m] = monthly_data.get(m, 0) + item['count']
        for item in msg_counts:
            m = item['month'].strftime('%b')
            monthly_data[m] = monthly_data.get(m, 0) + item['count']
        for item in part_counts:
            m = item['month'].strftime('%b')
            monthly_data[m] = monthly_data.get(m, 0) + item['count']

        # Ensure we have the last 6 months even if 0
        final_monthly_activity = []
        for i in range(5, -1, -1):
            month_date = timezone.now() - timedelta(days=i*30)
            m_name = month_date.strftime('%b')
            final_monthly_activity.append({
                'month': m_name,
                'total': monthly_data.get(m_name, 0)
            })

        data = {
            'programs_count': Program.objects.count(),
            'projects_count': Project.objects.count(),
            'volunteers_count': VolunteerApplication.objects.count(),
            'partnerships_count': PartnershipInquiry.objects.count(),
            'messages_count': ContactMessage.objects.count(),
            'impact_stories_count': ImpactStory.objects.count(),
            'unread_messages_count': ContactMessage.objects.filter(is_read=False).count(),
            'unread_partnerships_count': PartnershipInquiry.objects.filter(is_read=False).count(),
            'pending_volunteers_count': VolunteerApplication.objects.filter(status='pending').count(),
            'pending_partnerships_count': PartnershipInquiry.objects.filter(status='pending').count(),
            'monthly_activity': final_monthly_activity
        }
        return Response(data)
