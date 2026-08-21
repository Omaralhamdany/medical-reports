# management/commands/seed_hospitals.py

from django.core.management.base import BaseCommand
from django.core.files import File
from reports.models import Hospital
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'إضافة مستشفيات مع صورها'

    def handle(self, *args, **options):
        # قائمة المستشفيات مع مسارات الصور
        hospitals_data = [
            {
                'name_ar': 'مستشفى الملك فهد العام',
                'name_en': 'King Fahd General Hospital',
                'logo_path': 'hospital_logos/king_fahd.png',
            },
            {
                'name_ar': 'مستشفى الملك خالد',
                'name_en': 'King Khalid Hospital',
                'logo_path': 'hospital_logos/king_khalid.png',
            },
            {
                'name_ar': 'مستشفى الملك عبدالعزيز',
                'name_en': 'King Abdulaziz Hospital',
                'logo_path': 'hospital_logos/king_abdulaziz.png',
            },
            # أضف المزيد من المستشفيات هنا
        ]

        for hospital_data in hospitals_data:
            hospital, created = Hospital.objects.get_or_create(
                name_ar=hospital_data['name_ar'],
                defaults={
                    'name_en': hospital_data['name_en'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"✅ تم إنشاء المستشفى: {hospital.name_ar}")
            else:
                self.stdout.write(f"🔄 المستشفى موجود بالفعل: {hospital.name_ar}")
            
            # إضافة الشعار إذا كان موجوداً
            logo_path = Path('static/images') / hospital_data['logo_path']
            if logo_path.exists() and not hospital.logo:
                with open(logo_path, 'rb') as f:
                    hospital.logo.save(
                        f"{hospital_data['name_ar']}.png",
                        File(f),
                        save=True
                    )
                    self.stdout.write(f"   🖼️ تم إضافة الشعار لـ {hospital.name_ar}")