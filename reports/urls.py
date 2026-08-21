
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.views.generic import TemplateView
# from django.urls import path
from . import views 
from .views import (
    CreateReportView,
    CreateReportAPIView,
    ReportDetailView,
    ReportListView,
    SearchPatientAPIView,
    ReportSearchAPIView,
    ReportSearchAPIView,
    CreateHospitalView,
    ToggleReportStatusView,
)

app_name = 'reports'

urlpatterns = [
        # قائمة التقارير
    path('list/', views.ReportListView.as_view(), name='report_list'),
    # path('report/<int:report_id>/', views.report_detail, name='report_detail'),
        # صفحة إنشاء التقرير
    path('create/', CreateReportView.as_view(), name='create_report'),
    
    # API حفظ التقرير (POST)
    path('api/create/', CreateReportAPIView.as_view(), name='api_create_report'),
    
    path('<int:pk>/detail/', views.ReportDetailView.as_view(), name='report_detail'),
    # عرض التقرير النهائي
    path('<int:pk>/detail/', ReportDetailView.as_view(), name='report_detail'),
    
    # قائمة التقارير
    path('list/', ReportListView.as_view(), name='report_list'),
    
    # API البحث عن مريض
    path('api/search-patient/', SearchPatientAPIView.as_view(), name='api_search_patient'),

    # ===== صفحة الاستعلام =====
    path('inquiry/', TemplateView.as_view(template_name='reports/inquiry.html'), name='report_inquiry'),
    
    # ===== API البحث عن تقرير =====
    path('api/search/', ReportSearchAPIView.as_view(), name='api_report_search'),
    # path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('create/', CreateReportView.as_view(), name='create_report'),
    path('create_hospital/', CreateHospitalView.as_view(), name='create_hospital'),
    path('api/<int:report_id>/toggle-status/', ToggleReportStatusView.as_view(), name='toggle_report_status'),

]

# ✅ إضافة مسار الوسائط (لرفع الصور)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)