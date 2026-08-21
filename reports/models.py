from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date, timedelta
import random
import string

# ------------------------------------------------------------
# 1️⃣ نموذج المريض (Patients)
# ------------------------------------------------------------
class Patient(models.Model):
    """
    نموذج المرضى - يخزن المعلومات الأساسية للمريض
    """
    national_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="رقم الهوية / الإقامة",
        help_text="رقم الهوية الوطنية أو رقم الإقامة"
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name="الاسم الرباعي بالعربية"
    )
    name_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="الاسم بالإنجليزية"
    )
    nationality_ar = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="الجنسية بالعربية"
    )
    nationality_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="الجنسية بالإنجليزية"
    )
    relationship_ar = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="صلة القرابة بالعربية"
    )
    relationship_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="صلة القرابة بالإنجليزية"
    )
    employer = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="جهة العمل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "مريض"
        verbose_name_plural = "المرضى"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['name_ar']),
        ]

    def __str__(self):
        return f"{self.name_ar} ({self.national_id})"

    def get_full_name(self):
        """إرجاع الاسم الكامل بالعربية"""
        return self.name_ar

    def get_full_name_en(self):
        """إرجاع الاسم الكامل بالإنجليزية"""
        return self.name_en or self.name_ar


# ------------------------------------------------------------
# 2️⃣ نموذج الأطباء (Doctors)
# ------------------------------------------------------------
class Doctor(models.Model):
    """
    نموذج الأطباء - يخزن بيانات الأطباء
    """
    name_ar = models.CharField(
        max_length=100,
        verbose_name="اسم الطبيب بالعربية"
    )
    name_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="اسم الطبيب بالإنجليزية"
    )
    specialty_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="التخصص بالعربية"
    )
    specialty_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="التخصص بالإنجليزية"
    )
    license_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="رقم الترخيص الطبي"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar

    def get_full_name(self):
        return f"د. {self.name_ar}"


# ------------------------------------------------------------
# 3️⃣ نموذج المستشفيات (Hospitals)
# ------------------------------------------------------------
class Hospital(models.Model):
    """
    نموذج المستشفيات - يخزن بيانات المراكز الطبية
    """
    name_ar = models.CharField(
        max_length=150,
        verbose_name="اسم المستشفى بالعربية"
    )
    name_en = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="اسم المستشفى بالإنجليزية"
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="العنوان"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="رقم الهاتف"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    logo = models.ImageField(
        upload_to='hospital_logos/',
        blank=True,
        null=True,
        verbose_name="شعار المستشفى"
    )

    class Meta:
        verbose_name = "مستشفى"
        verbose_name_plural = "المستشفيات"
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar

      
    def get_logo_url(self):
        """إرجاع رابط الشعار"""
        if self.logo:
            return self.logo.url
        return None
# ------------------------------------------------------------
# 4️⃣ نموذج الأمراض (Diseases) - قائمة ثابتة للاختيار
# ------------------------------------------------------------
class Disease(models.Model):
    """
    نموذج الأمراض - قائمة ثابتة للأمراض الشائعة
    """
    name_ar = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="اسم المرض بالعربية"
    )
    name_en = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="اسم المرض بالإنجليزية"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="مفعل للعرض"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    class Meta:
        verbose_name = "مرض"
        verbose_name_plural = "الأمراض"
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar

    @classmethod
    def get_disease_choices(cls):
        """إرجاع قائمة الأمراض النشطة كخيارات للمنسدلة"""
        return [(d.name_ar, d.name_ar) for d in cls.objects.filter(is_active=True)]


# ------------------------------------------------------------
# 5️⃣ نموذج التقارير الطبية (Medical Reports) - الجدول الرئيسي
# ------------------------------------------------------------
class MedicalReport(models.Model):
    """
    نموذج التقارير الطبية - الجدول الرئيسي
    """

    # أنواع الإجازات
    LEAVE_TYPE_CHOICES = [
        ('حكومي', 'حكومي'),
        ('خاص', 'خاص'),
        ('شعار', 'شعار'),
    ]

    # --------------------------------------------------------
    # العلاقات (Foreign Keys)
    # --------------------------------------------------------
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_reports',
        verbose_name="المريض"
    )

    # --------------------------------------------------------
    # الحقول الأساسية
    # --------------------------------------------------------
    serial_no = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="الرقم التسلسلي"
    )
    leave_type = models.CharField(
        max_length=10,
        choices=LEAVE_TYPE_CHOICES,
        default='حكومي',
        verbose_name="نوع الإجازة"
    )

    # 🔥 حقل المرض من القائمة المنسدلة (اختياري)
    disease_type = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name="المرض المختار من القائمة"
    )

    # 🔥 حقل المرض المخصص (إذا اختار "أخرى")
    custom_disease = models.TextField(
        blank=True,
        null=True,
        verbose_name="المرض المخصص (نص حر)"
    )

     # 🔥 حقل جديد للتحكم في نشاط التقرير
    is_active = models.BooleanField(
        default=True,
        verbose_name="التقرير نشط",
        help_text="إذا كان غير نشط، لن يظهر في نتائج الاستعلام"
    )

    # --------------------------------------------------------
    # التواريخ
    # --------------------------------------------------------
    date_in = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ الدخول (ميلادي)"
    )
    date_in_formatted = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="التاريخ المنسق للدخول"
    )
    date_in_hijri = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="تاريخ الدخول (هجري)"
    )
    week_day = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="يوم الأسبوع"
    )

    date_out = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ الخروج (ميلادي)"
    )
    date_out_formatted = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="التاريخ المنسق للخروج"
    )
    date_out_hijri = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="تاريخ الخروج (هجري)"
    )
    days_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="عدد الأيام"
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ إصدار التقرير"
    )

    # --------------------------------------------------------
    # العلاقات Many-to-Many (عبر جداول وسيطة)
    # --------------------------------------------------------
    doctors = models.ManyToManyField(
        Doctor,
        through='ReportDoctor',
        related_name='reports',
        verbose_name="الأطباء"
    )
    hospitals = models.ManyToManyField(
        Hospital,
        through='ReportHospital',
        related_name='reports',
        verbose_name="المستشفيات"
    )

    # --------------------------------------------------------
    # الحقول الإضافية
    # --------------------------------------------------------
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات إضافية"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    barcode_data = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "تقرير طبي"
        verbose_name_plural = "التقارير الطبية"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['serial_no']),
            models.Index(fields=['date_in', 'date_out']),
            models.Index(fields=['patient', 'date_in']),
        ]

    def __str__(self):
        return f"{self.serial_no} - {self.patient.name_ar}"

    def save(self, *args, **kwargs):
        """توليد الرقم التسلسلي تلقائياً إذا لم يكن موجوداً"""
        if not self.serial_no:
            self.serial_no = self.generate_serial_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_serial_number():
        """توليد رقم تسلسلي فريد بصيغة GSL + السنة + أرقام عشوائية"""
        year = date.today().year
        random_digits = ''.join(random.choices(string.digits, k=6))
        return f"GSL{year}{random_digits}"

    def get_final_disease(self):
        """
        إرجاع المرض النهائي:
        - إذا كان هناك disease_type يرجعه
        - وإلا يرجح custom_disease
        """
        if self.disease_type:
            return self.disease_type.name_ar
        elif self.custom_disease:
            return self.custom_disease
        return "غير محدد"

    def get_final_disease_en(self):
        """إرجاع المرض النهائي بالإنجليزية"""
        if self.disease_type:
            return self.disease_type.name_en or self.disease_type.name_ar
        elif self.custom_disease:
            return self.custom_disease
        return "Not Specified"

    def calculate_days(self):
        """حساب عدد الأيام بين تاريخ الدخول والخروج"""
        if self.date_in and self.date_out:
            delta = self.date_out - self.date_in
            return delta.days + 1  # +1 لأن اليوم الأول يُحسب
        return 1

    def set_date_details(self, date_obj, prefix='date_in'):
        """
        تعيين تفاصيل التاريخ (منسق، هجري، يوم الأسبوع)
        يمكن استخدامها من views
        """
        if date_obj:
            # يمكن استخدام مكتبة مثل `hijri-converter` أو `django-hijri`
            # هذا مثال مبسط
            self.week_day = date_obj.strftime('%A')  # يوم الأسبوع بالإنجليزية

  
    def get_date_in_display(self):
        """الحصول على تاريخ الدخول المنسق"""
        if self.date_in_formatted:
            return self.date_in_formatted

        if self.date_in:
            return self.date_in.strftime('%d-%m-%Y')
        return '-'
    
    def get_date_out_display(self):
        """الحصول على تاريخ الخروج المنسق"""
        if self.date_out_formatted:
            return self.date_out_formatted
        if self.date_out:
            return self.date_out.strftime('%d-%m-%Y')
        return '-'
    
    def get_days_count_display(self):
        """الحصول على عدد الأيام بشكل صحيح"""
        if self.days_count and self.days_count > 0:
            return self.days_count
        if self.date_in and self.date_out:
            diff = (self.date_out - self.date_in).days
            return diff + 1 if diff >= 0 else 1
        return 1





# ------------------------------------------------------------
# 6️⃣ جدول وسيط: ربط التقرير بالطبيب (ReportDoctor)
# ------------------------------------------------------------
class ReportDoctor(models.Model):
    """
    نموذج وسيط لربط التقارير بالأطباء (Many-to-Many)
    """
    report = models.ForeignKey(
        MedicalReport,
        on_delete=models.CASCADE,
        related_name='report_doctors',
        verbose_name="التقرير"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='doctor_reports',
        verbose_name="الطبيب"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="الطبيب الرئيسي؟"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    class Meta:
        verbose_name = "طبيب التقرير"
        verbose_name_plural = "أطباء التقارير"
        unique_together = [['report', 'doctor']]
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.report.serial_no} - {self.doctor.name_ar}"


# ------------------------------------------------------------
# 7️⃣ جدول وسيط: ربط التقرير بالمستشفى (ReportHospital)
# ------------------------------------------------------------
class ReportHospital(models.Model):
    """
    نموذج وسيط لربط التقارير بالمستشفيات (Many-to-Many)
    """
    report = models.ForeignKey(
        MedicalReport,
        on_delete=models.CASCADE,
        related_name='report_hospitals',
        verbose_name="التقرير"
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='hospital_reports',
        verbose_name="المستشفى"
    )
    is_primary = models.BooleanField(
        default=True,
        verbose_name="المستشفى الرئيسي؟"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    class Meta:
        verbose_name = "مستشفى التقرير"
        verbose_name_plural = "مستشفيات التقارير"
        unique_together = [['report', 'hospital']]
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.report.serial_no} - {self.hospital.name_ar}"