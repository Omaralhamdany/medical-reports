# reports/deepl_translator.py

import deepl
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_translator():
    """الحصول على مترجم DeepL"""
    api_key = getattr(settings, 'DEEPL_API_KEY', None)
    if not api_key:
        return None
    
    try:
        return deepl.Translator(api_key)
    except Exception as e:
        logger.error(f"خطأ في تهيئة DeepL: {e}")
        return None


def translate_with_deepl(text, target_lang='EN-US', source_lang='AR'):
    """ترجمة باستخدام DeepL"""
    if not text:
        return text
    
    translator = get_translator()
    if not translator:
        return text
    
    try:
        result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
        return result.text
    except Exception as e:
        logger.error(f"خطأ في الترجمة: {e}")
        return text