from django.apps import AppConfig

class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    verbose_name = 'التقارير الطبية'

    def ready(self):
        import reports.signals
        """إنشاء الأمراض الأساسية عند بدء التشغيل"""
        try:
            from .models import Disease
            from django.db import connection
            
            # 🔥 التحقق من وجود الجدول قبل الوصول إليه
            table_name = Disease._meta.db_table
            if table_name in connection.introspection.table_names():
                if Disease.objects.count() == 0:
                    default_diseases = [
                        ('إصابة حادة في العظام والمفاصل', 'Acute Bone & Joint Injury'),
                        ('كسر مضاعف في العظام', 'Compound Bone Fracture'),
                        ('التواء شديد في الكاحل', 'Severe Ankle Sprain'),
                        ('انزلاق غضروفي قطني حاد', 'Acute Lumbar Disc Prolapse'),
                        ('شد عضلي حاد وفقرات الظهر', 'Acute Muscle Strain'),
                        ('نزلة معوية حادة وجفاف', 'Acute Gastroenteritis'),
                        ('التهاب جدار المعدة الحاد وقرحة', 'Acute Gastritis'),
                        ('مغص كلوي حاد مع حصوات', 'Acute Renal Colic'),
                        ('إنفلونزا حادة مع ارتفاع الحرارة', 'Severe Influenza'),
                        ('التهاب الحلق اللوزتين الحاد', 'Acute Tonsillitis'),
                        ('أزمة ربوية حادة وصعوبة تنفس', 'Acute Asthma Attack'),
                        ('إرهاق عام ووعكة صحية طارئة', 'General Fatigue'),
                    ]
                    for ar, en in default_diseases:
                        Disease.objects.get_or_create(
                            name_ar=ar,
                            defaults={'name_en': en, 'is_active': True}
                        )
                    print(f"✅ تم إنشاء {len(default_diseases)} مرض افتراضي")
        except Exception as e:
            # تجاهل الخطأ إذا كان الجدول غير موجود (في حالة الترحيلات الأولى)
            print(f"⚠️ لم يتم إنشاء الأمراض الافتراضية: {e}")