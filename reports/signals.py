from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicalReport
from .utils import save_barcode

@receiver(post_save, sender=MedicalReport)
def create_barcode(sender, instance, created, **kwargs):
    """إنشاء باركود تلقائياً عند إنشاء تقرير جديد"""
    if created or not instance.barcode_image:
        save_barcode(instance)
        instance.save()