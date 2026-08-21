"""
URL configuration for new_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse

# ============================================================
# عرض الصفحة الرئيسية (بدون قالب)
# ============================================================
def home_view(request):
    """
    الصفحة الرئيسية للمشروع - تعرض معلومات بسيطة
    """
    html = """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>نظام التقارير الطبية</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0e2f44, #1a5276);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
                direction: rtl;
            }
            .container {
                text-align: center;
                max-width: 800px;
            }
            .logo { font-size: 80px; margin-bottom: 20px; }
            h1 { font-size: 42px; margin-bottom: 10px; }
            .subtitle { font-size: 20px; opacity: 0.8; margin-bottom: 30px; }
            .cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .card {
                background: rgba(255,255,255,0.1);
                padding: 25px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: 0.3s;
                text-decoration: none;
                color: white;
            }
            .card:hover {
                transform: translateY(-5px);
                background: rgba(255,255,255,0.2);
            }
            .card .icon { font-size: 40px; display: block; margin-bottom: 10px; }
            .card h3 { margin: 0; font-size: 18px; }
            .card p { opacity: 0.7; font-size: 14px; margin-top: 8px; }
            .footer {
                margin-top: 40px;
                opacity: 0.5;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🏥</div>
            <h1>نظام التقارير الطبية</h1>
            <p class="subtitle">منصة متكاملة لإدارة التقارير الطبية والباركود</p>
            
            <div class="cards">

                <a href="/reports/create_hospital" style="display:inline-block; margin-top:10px; background:#2e86c1; color:white; padding:10px 15px; border-radius:8px; text-decoration:none;">
                + إضافة مستشفى جديد
                </a>
                <a href="/reports/create/" class="card">
                    <span class="icon">📝</span>
                    <h3>إنشاء تقرير جديد</h3>
                    <p>إدخال بيانات المريض والتشخيص</p>
                </a>
                <a href="/reports/list/" class="card">
                    <span class="icon">📂</span>
                    <h3>قائمة التقارير</h3>
                    <p>عرض جميع التقارير السابقة</p>
                </a>
                <a href="/admin/" class="card">
                    <span class="icon">⚙️</span>
                    <h3>لوحة التحكم</h3>
                    <p>إدارة النظام وقواعد البيانات</p>
                </a>
            </div>
            
            <div class="footer">
                © 2026 وزارة الصحة - جميع الحقوق محفوظة
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


# ============================================================
# مسارات URLs الرئيسية
# ============================================================
urlpatterns = [
    # ===== صفحة الإدارة =====
    path('admin/', admin.site.urls),
    
    # ===== الصفحة الرئيسية =====
    path('', home_view, name='home'),
    
    # ===== تطبيق التقارير الطبية =====
    path('reports/', include('reports.urls', namespace='reports')),
    
    # ===== إعادة التوجيه إلى الصفحة الرئيسية (اختياري) =====
    path('index/', RedirectView.as_view(url='/', permanent=True), name='index'),
]

# ============================================================
# إضافة مسارات الملفات الثابتة والوسائط (في وضع التطوير)
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # ===== إضافة واجهة Debug Toolbar (اختياري) =====
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]

# ============================================================
# معالجة الأخطاء المخصصة (اختياري)
# ============================================================
handler404 = 'reports.views.custom_404'  # يمكنك إنشاء هذا الـ View
handler500 = 'reports.views.custom_500'