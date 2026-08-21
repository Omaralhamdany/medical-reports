# reports/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Disease, Doctor, Hospital

@register(Disease)
class DiseaseTranslationOptions(TranslationOptions):
    fields = ('name_ar', 'name_en')  # الحقول التي تريد ترجمتها

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('name_ar', 'name_en', 'specialty_ar', 'specialty_en')

@register(Hospital)
class HospitalTranslationOptions(TranslationOptions):
    fields = ('name_ar', 'name_en')