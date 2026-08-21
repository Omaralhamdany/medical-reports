
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView  # 🔥 أضف TemplateView
from django.utils import timezone
from django.db import transaction
from django.db import models  # 🔥 أضف هذا للاستعلامات
import json
import random
import string
from datetime import datetime, date
from .utils import (
    translate_name,
    translate_with_deepl, 
    translate_medical_term,
    # translate_text,
    get_hospital_logo_url,
)
from .utils import translate_medical_term, translate_name

from .models import (
    Patient, Doctor, Hospital, Disease, 
    MedicalReport, ReportDoctor, ReportHospital
)

import json
import random
import string
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.utils import timezone
from django.db import transaction
from django.db import models

from .models import (
    Patient, Doctor, Hospital, Disease, 
    MedicalReport, ReportDoctor, ReportHospital
)

# استيراد دوال الترجمة من utils.py
from .utils import (
    translate_name,
    translate_medical_term,
    translate_with_deepl,
    get_hospital_logo_url,
    save_barcode,
)


# ============================================================
# 1️⃣ API View - استقبال البيانات وحفظها
# ============================================================

# views.py - تعديل CreateReportAPIView

class CreateReportAPIView(View):
    """
    API لاستقبال بيانات التقرير من الـ JavaScript وحفظها في قاعدة البيانات
    مع ترجمة تلقائية
    """
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # ===== استقبال البيانات من الـ request =====
            data = json.loads(request.body)
            
            # ===== استخراج البيانات مع معالجة القيم الفارغة =====
            def safe_str(value):
                """تحويل None إلى سلسلة فارغة مع إزالة المسافات الزائدة"""
                if value is None:
                    return ''
                return str(value).strip()
            
            # ===== استخراج البيانات بشكل آمن =====
            national_id = safe_str(data.get('nationalId'))
            name_ar = safe_str(data.get('nameAr'))
            name_en = safe_str(data.get('nameEn'))
            employer = safe_str(data.get('employer'))
            
            # 🔥🔥🔥 بيانات الجنسية 🔥🔥🔥
            nationality_ar = safe_str(data.get('nationality'))
            nationality_en = safe_str(data.get('nationalityEn'))
            
            # 🔥🔥🔥 بيانات صلة القرابة 🔥🔥🔥
            relationship_ar = safe_str(data.get('relationship'))
            relationship_en = safe_str(data.get('relationshipEn'))
            
            hospital_ar = safe_str(data.get('hospitalAr'))
            hospital_en = safe_str(data.get('hospitalEn'))
            hospital_id = data.get('hospitalId')
            
            specialty_ar = safe_str(data.get('specialty'))
            specialty_en = safe_str(data.get('specialtyEn'))
            
            disease_type = safe_str(data.get('diseaseType'))
            custom_disease = safe_str(data.get('customDisease'))
            disease_en = safe_str(data.get('diseaseEn'))
            
            # التواريخ
            date_in = safe_str(data.get('dateIn'))
            date_in_hijri = safe_str(data.get('dateInHijri'))
            date_out = safe_str(data.get('dateOut'))
            date_out_hijri = safe_str(data.get('dateOutHijri'))
            
            days_count = data.get('days', 1)
            week_day = safe_str(data.get('weekDay'))
            
            doctor_ar = safe_str(data.get('doctorAr'))
            doctor_en = safe_str(data.get('doctorEn'))
            notes = safe_str(data.get('notes'))
            
            # ============================================================
            # 🔥🔥🔥 الترجمة التلقائية 🔥🔥🔥
            # ============================================================
            
            print("=" * 50)
            print("🔍 بدء عملية الترجمة...")
            
            # 🔥 ترجمة التخصص
            if specialty_ar and not specialty_en:
                if ' / ' in specialty_ar:
                    specialty_ar_clean = specialty_ar.split(' / ')[0]
                else:
                    specialty_ar_clean = specialty_ar
                
                specialty_en = translate_medical_term(specialty_ar_clean)
                print(f"✅ ترجمة التخصص: '{specialty_ar_clean}' -> '{specialty_en}'")
            
            # 🔥 ترجمة اسم المريض
            if not name_en and name_ar:
                name_en = translate_name(name_ar)
                print(f"✅ ترجمة اسم المريض: '{name_ar}' -> '{name_en}'")
            
            # 🔥 ترجمة الجنسية
            if nationality_ar and not nationality_en:
                if ' / ' in nationality_ar:
                    nationality_en = nationality_ar.split(' / ')[1]
                else:
                    nationality_en = translate_medical_term(nationality_ar)
                print(f"✅ ترجمة الجنسية: '{nationality_ar}' -> '{nationality_en}'")
            
            # 🔥 ترجمة صلة القرابة
            if relationship_ar and not relationship_en:
                if ' / ' in relationship_ar:
                    relationship_en = relationship_ar.split(' / ')[1]
                else:
                    relationship_en = translate_medical_term(relationship_ar)
                print(f"✅ ترجمة صلة القرابة: '{relationship_ar}' -> '{relationship_en}'")
            
            # 🔥 ترجمة اسم المستشفى
            if not hospital_en and hospital_ar:
                hospital_en = translate_medical_term(hospital_ar)
                print(f"✅ ترجمة المستشفى: '{hospital_ar}' -> '{hospital_en}'")
            
            # 🔥 ترجمة اسم الطبيب
            if not doctor_en and doctor_ar:
                doctor_en = translate_name(doctor_ar)
                print(f"✅ ترجمة اسم الطبيب: '{doctor_ar}' -> '{doctor_en}'")
            
            # 🔥 ترجمة المرض المخصص
            if custom_disease and not disease_en:
                disease_en = translate_medical_term(custom_disease)
                print(f"✅ ترجمة المرض: '{custom_disease}' -> '{disease_en}'")
            
            print("✅ اكتملت الترجمة")
            print("=" * 50)
            
            # ===== التحقق من الحقول الإلزامية =====
            errors = []
            
            if not national_id:
                errors.append('رقم الهوية مطلوب')
            if not name_ar:
                errors.append('اسم المريض مطلوب')
            if not date_in:
                errors.append('تاريخ الدخول مطلوب')
            if not date_out:
                errors.append('تاريخ الخروج مطلوب')
            if not doctor_ar:
                errors.append('اسم الطبيب مطلوب')
            if not hospital_ar:
                errors.append('اسم المستشفى مطلوب')
            
            if errors:
                return JsonResponse({
                    'success': False,
                    'error': ' | '.join(errors)
                }, status=400)
            
            # ===== 1. إنشاء/جلب المريض مع حفظ الجنسية وصلة القرابة =====
            patient, created = Patient.objects.get_or_create(
                national_id=national_id,
                defaults={
                    'name_ar': name_ar,
                    'name_en': name_en if name_en else translate_name(name_ar),
                    'employer': employer,
                    'nationality_ar': nationality_ar,
                    'nationality_en': nationality_en if nationality_en else nationality_ar,
                    'relationship_ar': relationship_ar,
                    'relationship_en': relationship_en if relationship_en else relationship_ar,
                }
            )
            if not created:
                # تحديث البيانات إذا كان المريض موجوداً
                patient.name_ar = name_ar
                patient.name_en = name_en if name_en else translate_name(name_ar)
                patient.employer = employer if employer else patient.employer
                # 🔥 تحديث الجنسية وصلة القرابة
                if nationality_ar:
                    patient.nationality_ar = nationality_ar
                    patient.nationality_en = nationality_en if nationality_en else nationality_ar
                if relationship_ar:
                    patient.relationship_ar = relationship_ar
                    patient.relationship_en = relationship_en if relationship_en else relationship_ar
                patient.save()
            
            # ===== 2. إنشاء/جلب المستشفى =====
            hospital = None
            if hospital_id:
                try:
                    hospital = Hospital.objects.get(id=hospital_id)
                    print(f"✅ تم العثور على المستشفى: {hospital.name_ar}")
                except Hospital.DoesNotExist:
                    hospital, created = Hospital.objects.get_or_create(
                        name_ar=hospital_ar,
                        defaults={
                            'name_en': hospital_en if hospital_en else translate_medical_term(hospital_ar),
                            'is_active': True
                        }
                    )
            else:
                if hospital_ar:
                    hospital, created = Hospital.objects.get_or_create(
                        name_ar=hospital_ar,
                        defaults={
                            'name_en': hospital_en if hospital_en else translate_medical_term(hospital_ar),
                            'is_active': True
                        }
                    )
            
            # ===== 3. إنشاء/جلب الطبيب مع حفظ التخصص =====
            if specialty_ar and ' / ' in specialty_ar:
                specialty_ar_clean = specialty_ar.split(' / ')[0]
            else:
                specialty_ar_clean = specialty_ar if specialty_ar else 'طبيب عام'
            
            # 🔥 استخراج التخصص بالإنجليزية
            if not specialty_en and specialty_ar:
                if ' / ' in specialty_ar:
                    specialty_en = specialty_ar.split(' / ')[1]
                else:
                    specialty_en = translate_medical_term(specialty_ar_clean)
            
            doctor, _ = Doctor.objects.get_or_create(
                name_ar=doctor_ar,
                defaults={
                    'name_en': doctor_en if doctor_en else translate_name(doctor_ar),
                    'specialty_ar': specialty_ar_clean,
                    'specialty_en': specialty_en if specialty_en else translate_medical_term(specialty_ar_clean),
                    'is_active': True
                }
            )
            
            if specialty_ar_clean and doctor.specialty_ar != specialty_ar_clean:
                doctor.specialty_ar = specialty_ar_clean
                doctor.specialty_en = specialty_en if specialty_en else translate_medical_term(specialty_ar_clean)
                doctor.save()
            
            # ===== 4. التعامل مع المرض =====
            disease_obj = None
            
            if custom_disease:
                disease_obj, created = Disease.objects.get_or_create(
                    name_ar=custom_disease,
                    defaults={
                        'name_en': disease_en if disease_en else translate_medical_term(custom_disease)
                    }
                )
                if not created and not disease_obj.name_en:
                    disease_obj.name_en = disease_en if disease_en else translate_medical_term(custom_disease)
                    disease_obj.save()
                    
            elif disease_type and disease_type != 'CUSTOM':
                disease_obj, created = Disease.objects.get_or_create(
                    name_ar=disease_type,
                    defaults={
                        'name_en': disease_en if disease_en else disease_type
                    }
                )
                if not created and not disease_obj.name_en:
                    disease_obj.name_en = disease_en if disease_en else disease_type
                    disease_obj.save()
            
            # ===== 5. إنشاء التقرير الطبي =====
            serial_no = self.generate_serial_number()
            
            # تحويل التواريخ
            date_in_obj = None
            date_out_obj = None
            
            try:
                if date_in:
                    date_in_obj = datetime.strptime(date_in, '%d/%m/%Y').date()
            except (ValueError, TypeError):
                try:
                    if date_in:
                        date_in_obj = datetime.strptime(date_in, '%Y-%m-%d').date()
                except:
                    pass
            
            try:
                if date_out:
                    date_out_obj = datetime.strptime(date_out, '%d/%m/%Y').date()
            except (ValueError, TypeError):
                try:
                    if date_out:
                        date_out_obj = datetime.strptime(date_out, '%Y-%m-%d').date()
                except:
                    pass
            
            # حساب عدد الأيام
            days_count = 1
            if date_in_obj and date_out_obj:
                diff = (date_out_obj - date_in_obj).days
                days_count = diff + 1 if diff >= 0 else 1
            
            # إنشاء التقرير
            report = MedicalReport.objects.create(
                patient=patient,
                serial_no=serial_no,
                leave_type='حكومي',
                disease_type=disease_obj if disease_obj else None,
                custom_disease=custom_disease if custom_disease else None,
                date_in=date_in_obj,
                date_in_formatted=date_in,
                date_in_hijri=date_in_hijri if date_in_hijri else '',
                week_day=week_day if week_day else '',
                date_out=date_out_obj,
                date_out_formatted=date_out,
                date_out_hijri=date_out_hijri if date_out_hijri else '',
                days_count=days_count,
                issue_date=timezone.now().date(),
                notes=notes if notes else '',
            )
            
            # ===== إنشاء الباركود =====
            # save_barcode(report)
            report.save()
            
            # ===== 6. ربط التقرير بالطبيب =====
            ReportDoctor.objects.create(
                report=report,
                doctor=doctor,
                is_primary=True
            )
            
            # ===== 7. ربط التقرير بالمستشفى =====
            if hospital:
                ReportHospital.objects.create(
                    report=report,
                    hospital=hospital,
                    is_primary=True
                )
            
            # ===== 8. إرجاع البيانات المحفوظة =====
            return JsonResponse({
                'success': True,
                'message': 'تم حفظ التقرير بنجاح',
                'report_id': report.id,
                'serial_no': report.serial_no,
                'redirect_url': f'/reports/{report.id}/detail/',
                'debug': {
                    'specialty_ar': specialty_ar,
                    'specialty_en': specialty_en,
                    'name_ar': name_ar,
                    'name_en': name_en,
                    'hospital_ar': hospital_ar,
                    'hospital_en': hospital_en,
                    'doctor_ar': doctor_ar,
                    'doctor_en': doctor_en,
                    'nationality_ar': nationality_ar,
                    'nationality_en': nationality_en,
                    'relationship_ar': relationship_ar,
                    'relationship_en': relationship_en,
                }
            }, status=201)
            
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': False,
                'error': 'بيانات غير صالحة: ' + str(e)
            }, status=400)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def generate_serial_number(self):
        """توليد رقم تسلسلي فريد"""
        year = date.today().year
        random_digits = ''.join(random.choices(string.digits, k=6))
        serial = f"GSL{year}{random_digits}"
        while MedicalReport.objects.filter(serial_no=serial).exists():
            random_digits = ''.join(random.choices(string.digits, k=6))
            serial = f"GSL{year}{random_digits}"
        return serial



    def format_date(self, date_str):
        """تنسيق التاريخ بصيغة DD/MM/YYYY"""
        if not date_str:
            return None
        try:
            d = datetime.strptime(date_str, '%Y-%m-%d')
            return d.strftime('%d/%m/%Y')
        except:
            return None




# ============================================================
# 2️⃣ View عرض صفحة إنشاء التقرير (GET)
# ============================================================
# views.py

class CreateReportView(View):
    """
    عرض صفحة إنشاء التقرير الطبي (بدون فورم)
    """
    template_name = 'reports/create_report.html'
    
    def get(self, request, *args, **kwargs):
        # ===== جلب البيانات الأساسية للصفحة =====
        context = {
            # 🔥🔥🔥 جلب جميع المستشفيات النشطة مع صورها 🔥🔥🔥
            'hospitals': Hospital.objects.filter(is_active=True).order_by('name_ar'),
            
            # قائمة الأمراض للقائمة المنسدلة
            'diseases': Disease.objects.filter(is_active=True).order_by('name_ar'),
            
            # قائمة التخصصات للقائمة المنسدلة
            'specialties': [
                {'value': 'طبيب عام', 'label': 'طبيب عام'},
                {'value': 'أخصائي جراحة العظام', 'label': 'أخصائي جراحة العظام'},
                {'value': 'أخصائي الأمراض الباطنية', 'label': 'أخصائي الأمراض الباطنية'},
                {'value': 'أخصائي جراحة عامة', 'label': 'أخصائي جراحة عامة'},
                {'value': 'أخصائي طب الطوارئ', 'label': 'أخصائي طب الطوارئ'},
                {'value': 'أخصائي طب الأطفال', 'label': 'أخصائي طب الأطفال'},
                {'value': 'CUSTOM', 'label': '✨ أخرى - كتابة تخصص مخصص'},
            ],
            
            # بيانات افتراضية
            'default_hospital_ar': 'مستشفى الملك فهد العام التخصصي',
            'default_hospital_en': 'King Fahd General Specialist Hospital',
            'default_employer': 'وزارة الموارد البشرية والتمكين الاجتماعي',
            'today': timezone.now().date().isoformat(),
        }
        
        return render(request, self.template_name, context)


class ReportDetailView(DetailView):
    """
    عرض التقرير الطبي النهائي مع الباركود
    """
    model = MedicalReport
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'
    
    def get_queryset(self):
        """جلب التقرير مع جميع العلاقات المرتبطة لتحسين الأداء"""
        return MedicalReport.objects.select_related(
            'patient', 
            'disease_type'
        ).prefetch_related(
            'report_doctors__doctor',
            'report_hospitals__hospital'
        )
    
    def get_context_data(self, **kwargs):
        """إضافة البيانات الإضافية إلى سياق القالب"""
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        
        

        # ============================================================
        # 1️⃣ جلب الأطباء
        # ============================================================
        doctors = report.report_doctors.all()
        primary_doctor_obj = doctors.filter(is_primary=True).first()
        other_doctors_objs = doctors.filter(is_primary=False)
        
        # استخراج كائنات الأطباء
        primary_doctor = primary_doctor_obj.doctor if primary_doctor_obj else None
        other_doctors = [rd.doctor for rd in other_doctors_objs]
        
        # ============================================================
        # 2️⃣ جلب المستشفيات
        # ============================================================
        hospitals = report.report_hospitals.all()
        primary_hospital_obj = hospitals.filter(is_primary=True).first()
        other_hospitals_objs = hospitals.filter(is_primary=False)
        
        # استخراج كائنات المستشفيات
        primary_hospital = primary_hospital_obj.hospital if primary_hospital_obj else None
        other_hospitals = [rh.hospital for rh in other_hospitals_objs]
        
        # ============================================================
        # 3️⃣ المرض النهائي
        # ============================================================
        final_disease = report.get_final_disease()
        final_disease_en = report.get_final_disease_en()
        
        # ============================================================
        # 4️⃣ 🔥🔥🔥 الحصول على شعار المستشفى (المعدل) 🔥🔥🔥
        # ============================================================
        hospital_logo_url = None
        if primary_hospital:
            # ✅ تمرير كائن المستشفى وليس اسمه
            hospital_logo_url = get_hospital_logo_url(primary_hospital)
            print(f"🏥 شعار المستشفى: {primary_hospital.name_ar} -> {hospital_logo_url}")
        
        # ============================================================
        # 5️⃣ 🔥🔥🔥 طباعة بيانات التصحيح (DEBUG) 🔥🔥🔥
        # ============================================================
        print("=" * 60)
        print("📊 بيانات التقرير للعرض (ReportDetailView)")
        print("=" * 60)
        print(f"📝 الرقم التسلسلي: {report.serial_no}")
        print(f"📝 المرض (عربي): {final_disease}")
        print(f"📝 المرض (إنجليزي): {final_disease_en}")
        print("-" * 40)
        
        if primary_doctor:
            print(f"👨‍⚕️ الطبيب الرئيسي:")
            print(f"   - name_ar: {primary_doctor.name_ar}")
            print(f"   - name_en: {primary_doctor.name_en}")
            print(f"   - specialty_ar: {primary_doctor.specialty_ar}")
            print(f"   - specialty_en: {primary_doctor.specialty_en}")
        else:
            print("⚠️ لا يوجد طبيب رئيسي")
        
        print("-" * 40)
        
        if primary_hospital:
            print(f"🏥 المستشفى الرئيسي:")
            print(f"   - name_ar: {primary_hospital.name_ar}")
            print(f"   - name_en: {primary_hospital.name_en}")
            print(f"   - has_logo: {bool(primary_hospital.logo)}")
            print(f"   - logo_url: {hospital_logo_url}")
        else:
            print("⚠️ لا يوجد مستشفى رئيسي")
        
        print("-" * 40)
        print(f"📅 تاريخ الدخول: {report.get_date_in_display()}")
        print(f"📅 تاريخ الخروج: {report.get_date_out_display()}")
        print(f"📊 عدد الأيام: {report.get_days_count_display()}")
        print("=" * 60)
        
        # ============================================================
        # 6️⃣ تحديث السياق
        # ============================================================
        context.update({
            # الأطباء
            'primary_doctor': primary_doctor,
            'other_doctors': other_doctors,
            
            # المستشفيات
            'primary_hospital': primary_hospital,
            'other_hospitals': other_hospitals,
            
            # المرض
            'final_disease': final_disease,
            'final_disease_en': final_disease_en,
            
            # الباركود والشعار
            'barcode_data': report.serial_no,
            'hospital_logo_url': hospital_logo_url,  # ✅ رابط الشعار
            
            # 🔥 إضافة بيانات إضافية مفيدة للقالب
            'has_primary_doctor': primary_doctor is not None,
            'has_primary_hospital': primary_hospital is not None,
            'has_barcode': bool(report.barcode_image),
        })
        
        return context




# ============================================================
# 4️⃣ View قائمة التقارير (اختياري)
# ============================================================
class ReportListView(ListView):
    """
    عرض قائمة التقارير الطبية
    """
    model = MedicalReport
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        return MedicalReport.objects.select_related(
            'patient', 'disease_type'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = MedicalReport.objects.count()
        context['today_reports'] = MedicalReport.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        return context


# ============================================================
# 5️⃣ View بحث عن مريض (API - اختياري)
# ============================================================
class SearchPatientAPIView(View):
    """
    API للبحث عن مريض برقم الهوية
    """
    def get(self, request, *args, **kwargs):
        national_id = request.GET.get('national_id', '').strip()
        if not national_id:
            return JsonResponse({'error': 'رقم الهوية مطلوب'}, status=400)
        
        try:
            patient = Patient.objects.get(national_id=national_id)
            return JsonResponse({
                'exists': True,
                'id': patient.id,
                'name_ar': patient.name_ar,
                'name_en': patient.name_en,
                'nationality_ar': patient.nationality_ar,
                'nationality_en': patient.nationality_en,
                'employer': patient.employer,
            })
        except Patient.DoesNotExist:
            return JsonResponse({'exists': False}, status=404)



# ============================================================
# 10️⃣ View معالجة الأخطاء المخصصة
# ============================================================
def custom_404(request, exception):
    """
    صفحة خطأ 404 مخصصة
    """
    html = """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 - الصفحة غير موجودة</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f4f6f9;
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
                max-width: 500px;
            }
            .code { font-size: 80px; color: #1a5276; }
            h1 { font-size: 32px; color: #17202a; }
            p { color: #5d6d7e; }
            a { color: #1a5276; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="code">404</div>
            <h1>الصفحة غير موجودة</h1>
            <p>عذراً، الصفحة التي تبحث عنها غير متوفرة.</p>
            <p><a href="/">🏠 العودة إلى الرئيسية</a></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html, status=404)


def custom_500(request):
    """
    صفحة خطأ 500 مخصصة
    """
    html = """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>500 - خطأ في الخادم</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f4f6f9;
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
                max-width: 500px;
            }
            .code { font-size: 80px; color: #e74c3c; }
            h1 { font-size: 32px; color: #17202a; }
            p { color: #5d6d7e; }
            a { color: #1a5276; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="code">500</div>
            <h1>خطأ في الخادم</h1>
            <p>عذراً، حدث خطأ داخلي في الخادم. نعتذر عن الإزعاج.</p>
            <p><a href="/">🏠 العودة إلى الرئيسية</a></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html, status=500)
            

class ReportSearchAPIView(View):
    """
    API للبحث عن تقرير باستخدام رقم الخدمة ورقم الهوية معًا (يجب تطابق الاثنين)
    """
    def get(self, request, *args, **kwargs):
        service_number = request.GET.get('service_number', '').strip()
        national_id = request.GET.get('national_id', '').strip()

        print(f"🔍 بحث: service_number={service_number}, national_id={national_id}")

        # ===== التحقق من وجود الحقول =====
        if not service_number:
            return JsonResponse({
                'success': False,
                'error': 'يرجى إدخال رمز الخدمة'
            }, status=400)

        if not national_id:
            return JsonResponse({
                'success': False,
                'error': 'يرجى إدخال رقم الهوية'
            }, status=400)

        # ===== البحث في قاعدة البيانات - يجب تطابق الاثنين معًا =====
        queryset = MedicalReport.objects.select_related(
            'patient', 'disease_type'
        ).prefetch_related(
            'report_doctors__doctor',
            'report_hospitals__hospital'
        )

        # 🔥🔥🔥 الشرط الأساسي: تطابق رمز الخدمة ورقم الهوية معًا 🔥🔥🔥
        queryset = queryset.filter(
            serial_no__iexact=service_number,  # رمز الخدمة
            patient__national_id=national_id,   # رقم الهوية
            is_active=True                      # التقارير النشطة فقط
        )

        report = queryset.first()

        if not report:
            return JsonResponse({
                'success': False,
                'error': 'لا توجد بيانات مطابقة - تأكد من صحة رمز الخدمة ورقم الهوية'
            }, status=404)

        # ===== جلب البيانات =====
        primary_doctor = report.report_doctors.filter(is_primary=True).first()
        doctor_name = primary_doctor.doctor.name_ar if primary_doctor else None

        primary_hospital = report.report_hospitals.filter(is_primary=True).first()
        hospital_name = primary_hospital.hospital.name_ar if primary_hospital else None

        # 🔥 طباعة للتصحيح
        print(f"📊 التقرير: ID={report.id}")
        print(f"📅 date_in_formatted: {report.date_in_formatted}")
        print(f"📅 date_out_formatted: {report.date_out_formatted}")
        print(f"📅 date_in: {report.date_in}")
        print(f"📅 date_out: {report.date_out}")
        print(f"📊 days_count: {report.days_count}")

        # 🔥 استخدام الدوال المساعدة للحصول على التواريخ
        date_in_display = report.get_date_in_display()
        date_out_display = report.get_date_out_display()
        days_count = report.get_days_count_display()

        data = {
            'success': True,
            'report': {
                'id': report.id,
                'serial_no': report.serial_no,
                'patient_name': report.patient.name_ar,
                'patient_national_id': report.patient.national_id,
                'employer': report.patient.employer or '-',
                'disease': report.get_final_disease() or '-',
                'date_in': date_in_display,
                'date_in_hijri': report.date_in_hijri or '-',
                'date_out': date_out_display,
                'date_out_hijri': report.date_out_hijri or '-',
                'days_count': days_count,
                'issue_date': report.issue_date.strftime('%d/%m/%Y') if report.issue_date else '-',
                'doctor_name': doctor_name or '-',
                'doctor_specialty': primary_doctor.doctor.specialty_ar if primary_doctor else 'طبيب عام',
                'hospital': hospital_name or '-',
                'week_day': report.week_day or '-',
                'notes': report.notes or '-',
                'created_at': report.created_at.strftime('%d/%m/%Y %H:%M'),
                'leave_type': report.leave_type or '-',
            }
        }

        print(f"📤 البيانات المرسلة: {data}")

        return JsonResponse(data, status=200)




class CreateHospitalView(View):
    """
    صفحة لإضافة مستشفى مباشرة من الموقع بدل من لوحة الإدارة
    """
    template_name = 'reports/create_hospital.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name_ar = (request.POST.get('name_ar') or '').strip()
        name_en = (request.POST.get('name_en') or '').strip()
        address = (request.POST.get('address') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        logo = request.FILES.get('logo')

        if not name_ar:
            return render(request, self.template_name, {
                'error': 'اسم المستشفى بالعربية مطلوب',
                'name_ar': name_ar,
                'name_en': name_en,
                'address': address,
                'phone': phone,
            })

        hospital, created = Hospital.objects.get_or_create(
            name_ar=name_ar,
            defaults={
                'name_en': name_en,
                'address': address,
                'phone': phone,
                'logo': logo,
                'is_active': True,
            }
        )

        if not created:
            hospital.name_en = name_en or hospital.name_en
            hospital.address = address or hospital.address
            hospital.phone = phone or hospital.phone
            if logo:
                hospital.logo = logo
            hospital.is_active = True
            hospital.save()

        return redirect('reports:create_report')

# في views.py - إضافة API لتغيير حالة التقرير

class ToggleReportStatusView(View):
    """
    API لتغيير حالة التقرير (نشط / غير نشط)
    """
    def post(self, request, report_id, *args, **kwargs):
        try:
            report = get_object_or_404(MedicalReport, id=report_id)
            # تغيير الحالة
            report.is_active = not report.is_active
            report.save()
            
            status_text = "نشط" if report.is_active else "غير نشط"
            return JsonResponse({
                'success': True,
                'message': f'تم تغيير حالة التقرير إلى {status_text}',
                'is_active': report.is_active
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
