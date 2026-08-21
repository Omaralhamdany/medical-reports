from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Patient, Doctor, Hospital, Disease,
    MedicalReport, ReportDoctor, ReportHospital
)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'national_id', 'employer', 'created_at')
    search_fields = ('name_ar', 'national_id', 'name_en')
    list_filter = ('nationality_ar', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('المعلومات الشخصية', {
            'fields': ('national_id', 'name_ar', 'name_en', 
                      'nationality_ar', 'nationality_en')
        }),
        ('معلومات إضافية', {
            'fields': ('relationship_ar', 'relationship_en', 'employer')
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'specialty_ar', 'license_number', 'is_active')
    search_fields = ('name_ar', 'name_en', 'specialty_ar')
    list_filter = ('specialty_ar', 'is_active')


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'is_active', 'has_logo']
    list_filter = ['is_active']
    search_fields = ['name_ar', 'name_en']
    
    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True
    has_logo.short_description = "يوجد شعار"



# @admin.register(Hospital)
# class HospitalAdmin(admin.ModelAdmin):
#     list_display = ('name_ar', 'phone', 'is_active')
#     search_fields = ('name_ar', 'name_en', 'address')
#     list_filter = ('is_active',)

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'is_active')
    search_fields = ('name_ar', 'name_en')
    list_filter = ('is_active',)

class ReportDoctorInline(admin.TabularInline):
    model = ReportDoctor
    extra = 1
    autocomplete_fields = ['doctor']

class ReportHospitalInline(admin.TabularInline):
    model = ReportHospital
    extra = 1
    autocomplete_fields = ['hospital']

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = (
        'serial_no', 'patient', 'get_final_disease_display', 
        'date_in', 'date_out', 'days_count', 'leave_type'
    )
    search_fields = ('serial_no', 'patient__name_ar', 'patient__national_id')
    list_filter = ('leave_type', 'date_in', 'created_at')
    readonly_fields = ('serial_no', 'created_at', 'updated_at')
    inlines = [ReportDoctorInline, ReportHospitalInline]
    autocomplete_fields = ['patient', 'disease_type']
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('serial_no', 'patient', 'leave_type')
        }),
        ('المرض', {
            'fields': ('disease_type', 'custom_disease'),
            'description': 'اختر مرض من القائمة، أو اكتب مرض مخصص'
        }),
        ('التواريخ', {
            'fields': (
                'date_in', 'date_in_formatted', 'date_in_hijri', 'week_day',
                'date_out', 'date_out_formatted', 'date_out_hijri',
                'days_count', 'issue_date'
            )
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_final_disease_display(self, obj):
        """عرض المرض النهائي في القائمة"""
        return obj.get_final_disease()
    get_final_disease_display.short_description = "المرض النهائي"