# templatetags/hospital_tags.py

from django import template
from django.templatetags.static import static
from django.conf import settings
from reports.models import Hospital
import re

register = template.Library()

# قاموس تحويل الأرقام العربية إلى إنجليزية
ARABIC_TO_ENGLISH_NUMBERS = {
    '٠': '0',
    '١': '1',
    '٢': '2',
    '٣': '3',
    '٤': '4',
    '٥': '5',
    '٦': '6',
    '٧': '7',
    '٨': '8',
    '٩': '9',
}

def convert_arabic_numbers_to_english(text):
    """تحويل الأرقام العربية إلى أرقام إنجليزية"""
    if not text:
        return text
    for arabic, english in ARABIC_TO_ENGLISH_NUMBERS.items():
        text = text.replace(arabic, english)
    return text

@register.simple_tag
def hospital_logo(hospital_name):
    """إرجاع رابط شعار المستشفى بناءً على اسمه"""
    if not hospital_name:
        return static('images/hospital_logos/default.png')
    
    if hasattr(hospital_name, 'logo'):
        if hospital_name.logo:
            return hospital_name.logo.url
        return static('images/hospital_logos/default.png')
    
    if isinstance(hospital_name, str):
        try:
            hospital = Hospital.objects.filter(name_ar=hospital_name).first()
            if hospital and hospital.logo:
                return hospital.logo.url
        except:
            pass
    
    return static('images/hospital_logos/default.png')

@register.filter
def get_hospital_logo(hospital):
    """فلتر للحصول على رابط شعار المستشفى"""
    return hospital_logo(hospital)

# قاموس تحويل أسماء الأشهر الهجرية إلى أرقام
HIJRI_MONTHS = {
    'محرم': '01',
    'صفر': '02',
    'ربيع الأول': '03',
    'ربيع الآخر': '04',
    'جمادى الأولى': '05',
    'جمادى الآخرة': '06',
    'رجب': '07',
    'شعبان': '08',
    'رمضان': '09',
    'شوال': '10',
    'ذو القعدة': '11',
    'ذو الحجة': '12',
}

HIJRI_MONTHS_EXTRA = {
    'ربيع الاول': '03',
    'ربيع الثاني': '04',
    'ربيع الاوّل': '03',
    'ربيع الآخر': '04',
    'جمادى الاولى': '05',
    'جمادى الآخرة': '06',
    'جمادى الأولى': '05',
    'جمادى الثانية': '06',
    'ذو القعدة': '11',
    'ذو الحجة': '12',
}

@register.filter
def convert_hijri_month_to_number(date_string):
    """
    تحويل التاريخ الهجري إلى صيغة DD-MM-YYYY بالأرقام الإنجليزية
    مثال: ٢٢ صفر ١٤٤٨ هـ -> 22-02-1448
    """
    if not date_string or date_string == '-':
        return date_string
    
    date_string = str(date_string).strip()
    
    # 🔥 طباعة للتصحيح
    print(f"🔍 Original date: {date_string}")
    
    # 🔥 الخطوة 1: إزالة "هـ" أو "هجري"
    date_string = re.sub(r'\s*هـ\s*', '', date_string)
    date_string = re.sub(r'\s*هجري\s*', '', date_string)
    
    # 🔥 الخطوة 2: تحويل الأرقام العربية إلى إنجليزية مؤقتاً
    temp_string = date_string
    for arabic, english in ARABIC_TO_ENGLISH_NUMBERS.items():
        temp_string = temp_string.replace(arabic, english)
    
    print(f"🔍 After converting numbers: {temp_string}")
    
    # 🔥 الخطوة 3: محاولة استخراج اليوم والشهر والسنة
    # النمط: DD اسم شهر YYYY
    pattern = r'(\d{1,2})\s+([^\d]+)\s+(\d{4})'
    match = re.search(pattern, temp_string)
    
    if match:
        day = match.group(1).strip()
        month_name = match.group(2).strip()
        year = match.group(3).strip()
        
        print(f"🔍 Day: {day}, Month: {month_name}, Year: {year}")
        
        # 🔥 البحث عن رقم الشهر
        month_number = None
        
        # البحث في القاموس الرئيسي
        for key, value in HIJRI_MONTHS.items():
            if key in month_name:
                month_number = value
                print(f"✅ Found month: {key} -> {value}")
                break
        
        # إذا لم يتم العثور، ابحث في القاموس الإضافي
        if not month_number:
            for key, value in HIJRI_MONTHS_EXTRA.items():
                if key in month_name or month_name in key:
                    month_number = value
                    print(f"✅ Found month (extra): {key} -> {value}")
                    break
        
        # إذا لم يتم العثور على الشهر، استخدم 01 كافتراضي
        if not month_number:
            month_number = '01'
            print(f"⚠️ Month not found, using default: 01")
        
        # 🔥 التأكد من أن اليوم والشهر برقمين
        day = day.zfill(2)
        month_number = month_number.zfill(2)
        
        # 🔥 تحويل السنة إلى 4 أرقام
        if len(year) == 2:
            year = '14' + year
        
        # 🔥 إرجاع التاريخ بالتنسيق المطلوب (DD-MM-YYYY)
        result = f"{day}-{month_number}-{year}"
        print(f"✅ Result: {result}")
        return result
    
    # 🔥 إذا لم يتم العثور على نمط، حاول تحويل الأرقام فقط
    result = convert_arabic_numbers_to_english(date_string)
    print(f"⚠️ Fallback result: {result}")
    return result

@register.filter
def convert_to_english_numbers(text):
    """فلتر لتحويل الأرقام العربية في النص إلى أرقام إنجليزية"""
    if not text:
        return text
    return convert_arabic_numbers_to_english(str(text))












# # templatetags/hospital_tags.py

# from django import template
# from django.templatetags.static import static
# import os
# from django.conf import settings


# # templatetags/hospital_tags.py

# from django import template
# from django.templatetags.static import static
# from reports.models import Hospital

# register = template.Library()

# @register.simple_tag
# def hospital_logo(hospital_name):
#     """
#     إرجاع رابط شعار المستشفى بناءً على اسمه
    
#     Args:
#         hospital_name: اسم المستشفى (str) أو كائن المستشفى
        
#     Returns:
#         str: رابط الشعار
#     """
#     if not hospital_name:
#         return static('images/hospital_logos/default.png')
    
#     # إذا كان كائن مستشفى
#     if hasattr(hospital_name, 'logo'):
#         if hospital_name.logo:
#             return hospital_name.logo.url
#         return static('images/hospital_logos/default.png')
    
#     # إذا كان اسم مستشفى
#     if isinstance(hospital_name, str):
#         try:
#             hospital = Hospital.objects.filter(name_ar=hospital_name).first()
#             if hospital and hospital.logo:
#                 return hospital.logo.url
#         except:
#             pass
    
#     return static('images/hospital_logos/default.png')

# @register.filter
# def get_hospital_logo(hospital):
#     """فلتر للحصول على رابط شعار المستشفى"""
#     return hospital_logo(hospital)



# # hospital_tags.py

# from django import template
# from django.utils.safestring import mark_safe
# import re

# register = template.Library()

# # قاموس تحويل أسماء الأشهر الهجرية إلى أرقام
# HIJRI_MONTHS = {
#     'محرم': '1',
#     'صفر': '2',
#     'ربيع الأول': '3',
#     'ربيع الآخر': '4',
#     'جمادى الأولى': '5',
#     'جمادى الآخرة': '6',
#     'رجب': '7',
#     'شعبان': '8',
#     'رمضان': '9',
#     'شوال': '10',
#     'ذو القعدة': '11',
#     'ذو الحجة': '12',
# }

# # معكوس القاموس للأسماء المختصرة أو المختلفة
# HIJRI_MONTHS_EXTRA = {
#     'ربيع الاول': '3',
#     'ربيع الثاني': '4',
#     'ربيع الاوّل': '3',
#     'ربيع الآخر': '4',
#     'جمادى الاولى': '5',
#     'جمادى الآخرة': '6',
#     'جمادى الأولى': '5',
#     'جمادى الثانية': '6',
#     'ذو القعدة': '11',
#     'ذو الحجة': '12',
# }

# @register.filter
# def convert_hijri_month_to_number(date_string):
#     """
#     تحويل التاريخ الهجري من صيغة (يوم + اسم شهر + سنة) إلى (يوم + رقم شهر + سنة)
#     مثال: 16-02-1448 -> 16-02-1448 (محرم -> 1, صفر -> 2, إلخ)
#     """
#     if not date_string or date_string == '-':
#         return date_string
    
#     # محاولة تحويل التاريخ إذا كان بصيغة DD-MM-YYYY أو DD/MM/YYYY
#     # نبحث عن اسم الشهر في النص
#     date_string = str(date_string)
    
#     # جرب أنماط مختلفة للتاريخ الهجري
#     # النمط: يوم - شهر - سنة (مع أو بدون مسافات)
#     patterns = [
#         r'(\d+)\s*[-/]\s*([^\d\-/]+)\s*[-/]\s*(\d+)',  # يوم - اسم شهر - سنة
#         r'(\d+)\s+([^\d]+)\s+(\d+)',  # يوم اسم شهر سنة (بدون فواصل)
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, date_string)
#         if match:
#             day = match.group(1).strip()
#             month_name = match.group(2).strip()
#             year = match.group(3).strip()
            
#             # البحث عن رقم الشهر
#             month_number = None
            
#             # التحقق من القاموس الرئيسي
#             for key, value in HIJRI_MONTHS.items():
#                 if key in month_name:
#                     month_number = value
#                     break
            
#             # إذا لم يتم العثور، تحقق من القاموس الإضافي
#             if not month_number:
#                 for key, value in HIJRI_MONTHS_EXTRA.items():
#                     if key in month_name or month_name in key:
#                         month_number = value
#                         break
            
#             # إذا تم العثور على رقم الشهر، قم بتنسيق التاريخ الجديد
#             if month_number:
#                 # تأكد من أن اليوم والشهر والسنة بتنسيق صحيح
#                 day = day.zfill(2)
#                 month_number = month_number.zfill(2)
                
#                 # إرجاع التاريخ بالتنسيق الجديد (يوم-شهر-سنة)
#                 return f"{day}-{month_number}-{year}"
    
#     # إذا لم يتم العثور على تطابق، أرجع النص الأصلي
#     return date_string

# @register.filter
# def format_hijri_date_with_numbers(date_string):
#     """
#     تنسيق التاريخ الهجري بالأرقام فقط (عكس convert_hijri_month_to_number)
#     """
#     return convert_hijri_month_to_number(date_string)



# # # reports/templatetags/hospital_tags.py


# # register = template.Library()

# # @register.simple_tag
# # def hospital_logo(hospital_name):
# #     """
# #     علامة قالب لعرض شعار المستشفى
    
# #     الاستخدام في القالب:
# #     {% load hospital_tags %}
# #     <img src="{% hospital_logo report.hospital.name_ar %}" alt="شعار المستشفى">
# #     """
# #     if not hospital_name:
# #         return static('images/hospital_logos/default.png')
    
# #     # تنظيف الاسم
# #     clean_name = hospital_name.strip()
    
# #     # محاولة العثور على الصورة
# #     logo_filename = f"{clean_name}.png"
# #     logo_path = os.path.join('images/hospital_logos', logo_filename)
    
# #     # التحقق من وجود الصورة
# #     static_root = settings.STATIC_ROOT
# #     full_path = os.path.join(static_root, logo_path)
    
# #     if os.path.exists(full_path):
# #         return static(logo_path)
    
# #     # محاولة بدون "مستشفى"
# #     if clean_name.startswith('مستشفى '):
# #         short_name = clean_name.replace('مستشفى ', '')
# #         logo_filename = f"{short_name}.png"
# #         logo_path = os.path.join('images/hospital_logos', logo_filename)
# #         full_path = os.path.join(static_root, logo_path)
        
# #         if os.path.exists(full_path):
# #             return static(logo_path)
    
# #     # الشعار الافتراضي
# #     return static('images/hospital_logos/default.png')


# # @register.simple_tag
# # def hospital_logo_with_fallback(hospital_name, fallback_text='🏥'):
# #     """
# #     علامة قالب لعرض شعار المستشفى مع نص بديل
    
# #     الاستخدام في القالب:
# #     {% load hospital_tags %}
# #     {% hospital_logo_with_fallback report.hospital.name_ar %}
# #     """
# #     logo_url = hospital_logo(hospital_name)
    
# #     # إذا كان الشعار افتراضياً، اعرض نصاً بدلاً من الصورة
# #     if 'default.png' in logo_url:
# #         return f'<span style="font-size: 48px;">{fallback_text}</span>'
    
# #     return f'<img src="{logo_url}" alt="شعار المستشفى" style="max-height: 80px; max-width: 120px;">'