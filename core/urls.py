from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserViewSet
from programs.views import ProgramViewSet
from projects.views import ProjectViewSet
from blog.views import NewsViewSet
from gallery.views import GalleryViewSet
from contact.views import ContactMessageViewSet
from volunteers.views import VolunteerApplicationViewSet
from partnerships.views import PartnershipInquiryViewSet
from impact.views import ImpactStoryViewSet
from core.views import DashboardSummaryView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'news', NewsViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'contact', ContactMessageViewSet)
router.register(r'volunteers', VolunteerApplicationViewSet)
router.register(r'partnerships', PartnershipInquiryViewSet)
router.register(r'impact-stories', ImpactStoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
