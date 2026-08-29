إرشادات النشر — PythonAnywhere (Backend) + Netlify (صفحة الاستعلام)

مقدّمة
-------
المشروع عبارة عن تطبيق Django كامل. الغرض هنا: نشر المشروع ككل على PythonAnywhere، ونشر صفحة الاستعلام المستقلة على Netlify التي تستدعي API البحث في PythonAnywhere.

تحضيرات محلية (قبل الرفع إلى GitHub)
-------------------------------------
1. تأكد أن كل التغييرات محلية مرفوعة إلى GitHub (أو استضافة Git أخرى).
   - git add .
   - git commit -m "Prepare for deployment: add deployment guides and production settings"
   - git push origin main

2. تأكد من وجود requirements.txt في جذر المشروع. (في المشروع الحالي موجود)
   - إذا أردت تحديثه من البيئة المحلية: pip freeze > requirements.txt

3. تأكد من أن settings.py يستخدم متغيرات البيئة:
   - SECRET_KEY, DEBUG, ALLOWED_HOSTS, DEEPL_API_KEY
   - في هذا المشروع تم بالفعل استخدام os.environ للحصول على SECRET_KEY و DEBUG و ALLOWED_HOSTS.


خطوات النشر على PythonAnywhere
------------------------------
(افتراض: لديك حساب وقد سجلت الدخول إلى https://www.pythonanywhere.com)

1) إعداد المجلد الخاص بالمشروع على PythonAnywhere
   - تسجيل الدخول → Consoles → Bash
   - استنساخ المشروع من GitHub (ضع رابط repo الخاص بك):
     git clone https://github.com/your-username/your-repo.git ~/your-repo
   - أو إن كنت قد رفعت الملفات يدوياً استخدم Files → Upload

2) إنشاء virtualenv
   - اختر نسخة بايثون متوافقة (مثلاً 3.11)
   - في الكونسول:
     python3.11 -m venv ~/.virtualenvs/myproject-venv
     source ~/.virtualenvs/myproject-venv/bin/activate
     pip install --upgrade pip
     pip install -r ~/your-repo/requirements.txt

3) إعداد Web app في PythonAnywhere
   - Web → Add a new web app → اختر Manual configuration → اختر Python 3.11
   - في قسم Virtualenv: أدخل المسار إلى virtualenv (مثال): /home/yourusername/.virtualenvs/myproject-venv
   - في Source code: ضع المسار إلى المشروع على PythonAnywhere (مثال): /home/yourusername/your-repo

4) تعديل ملف WSGI
   - افتح WSGI configuration file من صفحة Web tab
   - تأكد من تهيئة sys.path ليتضمن مجلد المشروع، وتفعيل virtualenv (عادة PythonAnywhere يضبطها من Web UI)
   - مثال تبسيطي داخل ملف WSGI (عدل المسارات حسب اسم المستخدم/المشروع):

     import os
     import sys

     path = '/home/yourusername/your-repo'
     if path not in sys.path:
         sys.path.insert(0, path)

     os.environ['DJANGO_SETTINGS_MODULE'] = 'New_project.settings'

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()

5) إعداد متغيرات البيئة و ALLOWED_HOSTS
   - في Web → Environment variables أضف:
     - SECRET_KEY = 'ضع_قيمة_آمنة_هنا'
     - DEBUG = False
     - ALLOWED_HOSTS = yourusername.pythonanywhere.com
     - DEEPL_API_KEY = (إذا كنت تستخدم DeepL)

6) إعداد static و media mappings في Web tab
   - Static files mappings:
     URL: /static/    Directory: /home/yourusername/your-repo/staticfiles
   - Media files mappings:
     URL: /media/     Directory: /home/yourusername/your-repo/media
   - تأكد من أن STATIC_ROOT في settings.py يطابق staticfiles path (موجود بالفعل في المشروع)

7) تشغيل أوامر إدارة Django
   - في Consoles افتح Bash وفعّل virtualenv
     source ~/.virtualenvs/myproject-venv/bin/activate
     cd ~/your-repo
     python manage.py migrate
     python manage.py collectstatic --noinput
     python manage.py createsuperuser   # أنشئ حساب إداري إذا أردت

8) Reload Web app
   - اضغط Reload في PythonAnywhere Web tab
   - افتح متصفح وزر عنوان: https://yourusername.pythonanywhere.com/ لتتأكد أن الموقع يعمل


نشر صفحة الاستعلام على Netlify
--------------------------------
1) افتح ملف inquiry_netlify/index.html في المستودع أو في جهازك
2) غيّر السطر التالي إلى دومين PythonAnywhere الحقيقي:
   const API_BASE = 'https://REPLACE_WITH_YOUR_PYTHONANYWHERE_DOMAIN';
   إلى مثال:
   const API_BASE = 'https://yourusername.pythonanywhere.com';
3) ادفع التغييرات إلى GitHub
4) في Netlify: New site → Import from Git
   - اختر المستودع الذي يحتوي على مجلد inquiry_netlify
   - ضمن Build command اتركها فارغة إن كانت صفحة ثابتة أو اجعل "" (Netlify سيستعمل ملفات كما هي)
   - Publish directory: inquiry_netlify
   - اختر فرع (branch) واضغط Deploy
5) بعد النشر اختبر الصفحة المنشورة بالاستعلام عن خدمة (ستستدعي API في PythonAnywhere).

نصائح أمان وأداء
-----------------
- استبدل Access-Control-Allow-Origin='*' في أي ردود CORS إلى رابط Netlify في الإعدادات أو استخدم django-cors-headers لإدارة CORS بشكل آمن.
- ضع DEBUG=False في الإنتاج.
- استخدم قاعدة بيانات مناسبة إن كان التطبيق يستخدم بيانات كبيرة (SQLite مقبول للتجارب الصغيرة، لكنه محدود في البيئات المتزامنة).
- حدّد معدل طلبات API (rate limiting) إذا كانت الخدمة معرضة للاستدعاء العام بكثافة.

هل أتابع الآن وأجري التعديلات التالية في المستودع:
- إضافة ملف DEPLOYMENT_PYTHONANYWHERE_AND_NETLIFY.md (تم إضافته الآن)،
- تحديث settings أو إضافة ملف .env.example إذا رغبت،
- تشغيل commit للتغييرات الحالية ورفعها إلى الفرع 'main'؟

أخبرني إذا تود المواصلة الآن بأحد الخيارات أعلاه (أجري commit وادفع التغييرات أو أعطيك الأوامر لتنفيذها محلياً).