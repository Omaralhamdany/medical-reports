# reports/utils.py

import qrcode
import deepl
import os
import logging
from django.conf import settings
from django.core.files.base import ContentFile
from django.templatetags.static import static
from io import BytesIO

logger = logging.getLogger(__name__)


# ============================================================
# 1️⃣ دوال الباركود والـ QR Code
# ============================================================

def save_barcode(instance):
    """
    إنشاء وحفظ باركود QR للتقرير الطبي
    """
    if not instance.barcode_image:
        url = f"https://www.seha.sa/#/inquiries/slenquiry?code={instance.serial_no}"
        
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=1,
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        instance.barcode_image.save(
            f"qr_{instance.id}.png",
            ContentFile(buffer.getvalue()),
            save=False
        )


# ============================================================
# 2️⃣ قاموس المصطلحات الطبية (للترجمة السريعة)
# ============================================================

MEDICAL_TERMS = {
    # ===== التخصصات الطبية =====
    "اخصائي قلب": "Cardiologist",
    "أخصائي قلب": "Cardiologist",
    "اخصائي قلبية": "Cardiologist",
    "أخصائي قلبية": "Cardiologist",
    "اخصائي القلب": "Cardiologist",
    "أخصائي القلب": "Cardiologist",
    "طبيب قلب": "Cardiologist",
    "اخصائي جراحة القلب": "Cardiac Surgeon",
    "أخصائي جراحة القلب": "Cardiac Surgeon",
    "جراح قلب": "Cardiac Surgeon",
    "اخصائي عظام": "Orthopedic Specialist",
    "أخصائي عظام": "Orthopedic Specialist",
    "اخصائي جراحة العظام": "Orthopedic Surgeon",
    "أخصائي جراحة العظام": "Orthopedic Surgeon",
    "جراح عظام": "Orthopedic Surgeon",
    "اخصائي باطنية": "Internal Medicine Specialist",
    "أخصائي باطنية": "Internal Medicine Specialist",
    "طبيب باطنية": "Internist",
    "اخصائي أطفال": "Pediatrician",
    "أخصائي أطفال": "Pediatrician",
    "طبيب أطفال": "Pediatrician",
    "اخصائي أعصاب": "Neurologist",
    "أخصائي أعصاب": "Neurologist",
    "اخصائي جراحة أعصاب": "Neurosurgeon",
    "أخصائي جراحة أعصاب": "Neurosurgeon",
    "جراح أعصاب": "Neurosurgeon",
    "اخصائي عيون": "Ophthalmologist",
    "أخصائي عيون": "Ophthalmologist",
    "طبيب عيون": "Ophthalmologist",
    "اخصائي انف واذن وحنجرة": "ENT Specialist",
    "أخصائي أنف وأذن وحنجرة": "ENT Specialist",
    "طبيب انف واذن وحنجرة": "ENT Specialist",
    "اخصائي جلدية": "Dermatologist",
    "أخصائي جلدية": "Dermatologist",
    "طبيب جلدية": "Dermatologist",
    "اخصائي نساء وولادة": "Obstetrician-Gynecologist",
    "أخصائي نساء وولادة": "Obstetrician-Gynecologist",
    "طبيب نساء وولادة": "Obstetrician-Gynecologist",
    "اخصائي مسالك بولية": "Urologist",
    "أخصائي مسالك بولية": "Urologist",
    "طبيب مسالك بولية": "Urologist",
    "اخصائي جراحة عامة": "General Surgeon",
    "أخصائي جراحة عامة": "General Surgeon",
    "جراح عام": "General Surgeon",
    "اخصائي تخدير": "Anesthesiologist",
    "أخصائي تخدير": "Anesthesiologist",
    "طبيب تخدير": "Anesthesiologist",
    "اخصائي اشعة": "Radiologist",
    "أخصائي أشعة": "Radiologist",
    "طبيب اشعة": "Radiologist",
    "اخصائي طوارئ": "Emergency Medicine Specialist",
    "أخصائي طوارئ": "Emergency Medicine Specialist",
    "طبيب طوارئ": "Emergency Physician",
    "اخصائي طب الاسرة": "Family Medicine Specialist",
    "أخصائي طب الأسرة": "Family Medicine Specialist",
    "طبيب اسرة": "Family Physician",
    "طبيب عام": "General Practitioner",
    "استشاري": "Consultant",
    "جراح": "Surgeon",
    "اخصائي": "Specialist",
    
    # ===== الأمراض والحالات =====
    "انفلونزا حادة": "Severe Influenza",
    "إنفلونزا حادة": "Severe Influenza",
    "كسر مضاعف": "Compound Fracture",
    "اصابة حادة": "Acute Injury",
    "إصابة حادة": "Acute Injury",
    "انزلاق غضروفي": "Disc Prolapse",
    "التواء شديد": "Severe Sprain",
    "شد عضلي": "Muscle Strain",
    "نزلة معوية": "Gastroenteritis",
    "مغص كلوي": "Renal Colic",
    "ازمة ربوية": "Asthma Attack",
    "أزمة ربوية": "Asthma Attack",
    "ارتفاع الحرارة": "Fever",
    "التهاب الحلق": "Tonsillitis",
    "التهاب المعدة": "Gastritis",
    "قرحة": "Ulcer",
    "حصوات": "Stones",
    "كسر": "Fracture",
    "التهاب": "Inflammation",
    "عدوى": "Infection",
    "فيروس": "Virus",
    "بكتيريا": "Bacteria",
    "إصابة": "Injury",
    "ألم": "Pain",
    "صداع": "Headache",
    "حمى": "Fever",
    "سعال": "Cough",
    "ضيق تنفس": "Shortness of Breath",
    
    # ===== المستشفيات =====
    "مستشفى الملك فهد العام": "King Fahd General Hospital",
    "مستشفى الملك فهد التخصصي": "King Fahd Specialist Hospital",
    "مستشفى الملك خالد": "King Khalid Hospital",
    "مستشفى الملك عبدالعزيز": "King Abdulaziz Hospital",
    "مستشفى الملك فيصل": "King Faisal Hospital",
    "مستشفى الحرس الوطني": "National Guard Hospital",
    "مستشفى القوات المسلحة": "Armed Forces Hospital",
}


# ============================================================
# 3️⃣ قاموس الأسماء العربية
# ============================================================

ARABIC_NAMES = {
    "محمد": "Mohammed",
    "أحمد": "Ahmed",
    "احمد": "Ahmed",
    "علي": "Ali",
    "عمر": "Omar",
    "عمرو": "Amr",
    "خالد": "Khaled",
    "عبدالله": "Abdullah",
    "عبدالرحمن": "Abdulrahman",
    "عبدالعزيز": "Abdulaziz",
    "عبدالملك": "Abdulmalik",
    "عبدالوهاب": "Abdulwahab",
    "عبدالرزاق": "Abdulrazak",
    "عبدالقادر": "Abdulkader",
    "عبداللطيف": "Abdullatif",
    "عبدالكريم": "Abdulkarim",
    "عبدالمحسن": "Abdulmohsen",
    "عبدالرحيم": "Abdulrahim",
    "عبدالسلام": "Abdulsalam",
    "عبدالمجيد": "Abdulmajid",
    "عبدالحميد": "Abdulhamid",
    "عبدالفتاح": "Abdulfattah",
    "عبدالهادي": "Abdulhadi",
    "عبدالناصر": "Abdulnasser",
    "عبدالغني": "Abdulghani",
    "عبدالصمد": "Abdulsamad",
    "عبدالودود": "Abdulwadood",
    "عبدالغفور": "Abdulghafoor",
    "سعود": "Saud",
    "فهد": "Fahd",
    "ناصر": "Naser",
    "سعيد": "Saeed",
    "ماجد": "Majed",
    "سلطان": "Sultan",
    "فيصل": "Faisal",
    "تركي": "Turki",
    "بدر": "Badr",
    "حسن": "Hassan",
    "حسين": "Hussein",
    "زيد": "Zaid",
    "سالم": "Salem",
    "طلال": "Talal",
    "منصور": "Mansour",
    "راشد": "Rashid",
    "مبارك": "Mubarak",
    "إبراهيم": "Ibrahim",
    "اسماعيل": "Ismail",
    "يعقوب": "Yacoub",
    "يوسف": "Yousef",
    "موسى": "Mousa",
    "عيسى": "Isa",
    "داود": "Dawood",
    "سليمان": "Suleiman",
    "ايوب": "Ayoub",
    "يونس": "Younis",
    "نوح": "Noah",
    "ادم": "Adam",
    "حمزة": "Hamza",
    "بسام": "Bassam",
    "سامي": "Sami",
    "زيدان": "Zaidan",
    "مازن": "Mazen",
    "نواف": "Nawaf",
    "مشعل": "Mishal",
}


# ============================================================
# 4️⃣ دوال الترجمة
# ============================================================

def get_deepl_translator():
    """
    إنشاء كائن مترجم DeepL
    """
    api_key = getattr(settings, 'DEEPL_API_KEY', None)
    if not api_key:
        logger.warning("⚠️ DEEPL_API_KEY غير مضبوط في الإعدادات")
        return None
    
    try:
        use_free = getattr(settings, 'DEEPL_USE_FREE_API', True)
        
        if use_free:
            translator = deepl.Translator(api_key)
        else:
            translator = deepl.Translator(api_key, server_url='https://api.deepl.com')
        
        logger.info("✅ تم تهيئة DeepL Translator بنجاح")
        return translator
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة DeepL: {e}")
        return None


def translate_with_deepl(text, target_lang='EN-US', source_lang='AR'):
    """
    ترجمة النص باستخدام DeepL API
    """
    if not text or not text.strip():
        return text
    
    translator = get_deepl_translator()
    if not translator:
        logger.warning("⚠️ DeepL غير متوفر، إرجاع النص الأصلي")
        return text
    
    try:
        result = translator.translate_text(
            text,
            target_lang=target_lang,
            source_lang=source_lang
        )
        logger.info(f"✅ ترجمة DeepL: '{text}' -> '{result.text}'")
        return result.text
    except Exception as e:
        logger.error(f"❌ خطأ في ترجمة DeepL: {e}")
        return text


def translate_medical_term(text):
    """
    ترجمة المصطلحات الطبية
    """
    if not text:
        return text
    
    text_clean = text.strip()
    
    # 🔥 البحث عن تطابق تام
    if text_clean in MEDICAL_TERMS:
        result = MEDICAL_TERMS[text_clean]
        logger.info(f"✅ ترجمة من القاموس: '{text_clean}' -> '{result}'")
        return result
    
    # 🔥 البحث عن تطابق غير حساس لحالة الأحرف
    for ar_term, en_term in MEDICAL_TERMS.items():
        if ar_term.lower() == text_clean.lower():
            logger.info(f"✅ ترجمة (غير حساسة): '{text_clean}' -> '{en_term}'")
            return en_term
    
    # 🔥 البحث عن تطابق جزئي
    for ar_term, en_term in MEDICAL_TERMS.items():
        if ar_term in text_clean or text_clean in ar_term:
            logger.info(f"✅ ترجمة (تطابق جزئي): '{text_clean}' -> '{en_term}'")
            return en_term
    
    # 🔥 إذا لم يوجد في القاموس، نستخدم DeepL
    logger.info(f"🔍 لم يتم العثور في القاموس، استخدام DeepL: '{text_clean}'")
    return translate_with_deepl(text_clean, target_lang='EN-US')


def translate_name(arabic_name):
    """
    ترجمة الاسم العربي إلى الإنجليزية
    """
    if not arabic_name:
        return arabic_name
    
    text_clean = arabic_name.strip()
    
    # 🔥 البحث عن تطابق تام
    if text_clean in ARABIC_NAMES:
        return ARABIC_NAMES[text_clean]
    
    # 🔥 ترجمة كل كلمة على حدة
    words = text_clean.split()
    translated_words = []
    
    for word in words:
        if word in ARABIC_NAMES:
            translated_words.append(ARABIC_NAMES[word])
        else:
            # محاولة ترجمة الكلمة باستخدام DeepL
            translated = translate_with_deepl(word, target_lang='EN-US')
            translated_words.append(translated if translated else word)
    
    return " ".join(translated_words)


# ============================================================
# 5️⃣ دوال شعارات المستشفيات
# ============================================================


# utils.py

def get_hospital_logo_url(hospital):
    """
    الحصول على رابط شعار المستشفى من قاعدة البيانات
    
    Args:
        hospital: كائن المستشفى (Hospital instance) أو اسم المستشفى (str)
        
    Returns:
        str: رابط الشعار أو None
    """
    if not hospital:
        return None
    
    # ✅ إذا كان الكائن من نوع Hospital
    if hasattr(hospital, 'logo'):
        if hospital.logo:
            return hospital.logo.url
        return None
    
    # ✅ إذا كان نص (اسم المستشفى) - للتوافق مع الإصدارات القديمة
    if isinstance(hospital, str):
        # محاولة البحث عن المستشفى في قاعدة البيانات
        try:
            from .models import Hospital
            hospital_obj = Hospital.objects.filter(name_ar=hospital).first()
            if hospital_obj and hospital_obj.logo:
                return hospital_obj.logo.url
        except:
            pass
        return None
    
    return None

