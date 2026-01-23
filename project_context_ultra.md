CONTEXT: Django Project. Comments removed for brevity. Interpret code logic.

# TREE
./
  auto_test.py
  export_project.py
  reset_db.py
  setup_initial_data.py
  apps/
    api/
      apps.py
      serializers.py
      urls.py
      views.py
      __init__.py
    automation/
      admin.py
      apps.py
      models.py
      services.py
      signals.py
      tasks.py
      urls.py
      views.py
      __init__.py
      management/
        __init__.py
        commands/
          runbot.py
          setup_templates.py
          __init__.py
    core/
      admin.py
      apps.py
      audit.py
      context_processors.py
      dashboards.py
      export_views.py
      history_views.py
      middleware.py
      mixins.py
      models.py
      services.py
      tasks.py
      urls.py
      utils.py
      views.py
      __init__.py
      management/
        commands/
          audit_system.py
    crm/
      admin.py
      apps.py
      forms.py
      htmx_views.py
      models.py
      services.py
      urls.py
      views.py
      __init__.py
    education/
      admin.py
      apps.py
      forms.py
      lms.py
      lms_models.py
      lms_views.py
      materials.py
      materials_views.py
      models.py
      services.py
      urls.py
      views.py
      __init__.py
      services/
        journal.py
        scheduling.py
        __init__.py
    finance/
      admin.py
      apps.py
      cash_register.py
      forms.py
      inventory.py
      inventory_views.py
      models.py
      payroll.py
      payroll_views.py
      selectors.py
      services.py
      signals.py
      urls.py
      views.py
      __init__.py
    operations/
      admin.py
      apps.py
      gamification.py
      models.py
      schedule.py
      services.py
      shop.py
      shop_views.py
      tasks.py
      urls.py
      views.py
      __init__.py
    organizations/
      admin.py
      apps.py
      models.py
      services.py
      urls.py
      views.py
      __init__.py
    users/
      admin.py
      apps.py
      forms.py
      managers.py
      models.py
      permissions.py
      services.py
      urls.py
      views.py
      __init__.py
  config/
    asgi.py
    celery.py
    urls.py
    wsgi.py
    __init__.py
    settings/
      base.py
      local.py
      production.py
      __init__.py
  requirements/
  static/
    css/
      style.css
    img/
    js/
      alpine.min.js
      app.js
      htmx.min.js
    vendors/
  templates/
    base.html
    dashboard.html
    automation/
      template_form.html
      template_list.html
    components/
      modal.html
      navbar.html
      search_results.html
      sidebar.html
      toast.html
      forms/
    core/
      history.html
    crm/
      lead_convert.html
      lead_detail.html
      lead_form.html
      pipeline.html
      source_list.html
      stage_form.html
      stage_list.html
      partials/
    dashboards/
      admin.html
      parent.html
      staff.html
      student.html
      super_admin.html
      teacher.html
    education/
      course_list.html
      form.html
      group_detail.html
      group_form.html
      group_list.html
      materials.html
      room_list.html
    finance/
      account_form.html
      account_list.html
      payroll_calculate.html
      payroll_list.html
      pending_receipts.html
      report.html
      staff_attendance.html
      student_payments.html
      student_payment_form.html
      supply_list.html
      transaction_form.html
      transaction_list.html
    layouts/
    operations/
      lesson_list.html
      purchase_history.html
      schedule.html
      shop.html
      shop_admin.html
      student_ratings.html
      take_attendance.html
      teacher_ratings.html
    registration/
      login.html
    users/
      user_confirm_delete.html
      user_form.html
      user_list.html
  tests/
    factories.py
    test_finance.py
    test_scheduling.py

# CODE
--- auto_test.py ---
import time
from colorama import init, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
init(autoreset=True)
BASE_URL = "http://127.0.0.1:8000"
ADMIN_PHONE = "998900000000"
ADMIN_PASS = "admin"
class RobustTester:
    def __init__(self):
        print(f"{Fore.CYAN}🛡️ MUSTAHKAM TEST BOSHLANDI...{Style.RESET_ALL}")
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 3)
        self.errors = []
        self.success_count = 0
    def log_success(self, msg):
        print(f"{Fore.GREEN}✅ [OK] {msg}")
        self.success_count += 1
    def log_fail(self, msg, error_details=""):
        print(f"{Fore.RED}❌ [FAIL] {msg}")
        if error_details:
            print(f"   Original Error: {str(error_details)[:100]}...")
        self.errors.append(msg)
    def safe_action(self, description, action_func):
        try:
            action_func()
            self.log_success(description)
        except Exception as e:
            self.log_fail(description, e)
    def _login(self):
        self.driver.get(f"{BASE_URL}/login/")
        self.driver.find_element(By.NAME, "username").send_keys(ADMIN_PHONE)
        self.driver.find_element(By.NAME, "password").send_keys(ADMIN_PASS)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        if "login" in self.driver.current_url:
            raise Exception("Login url o'zgarmadi")
    def _check_dashboard(self):
        self.driver.get(f"{BASE_URL}/")
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        if "Xush kelibsiz" not in body_text and "Dashboard" not in body_text:
            raise Exception("Dashboard matni topilmadi")
    def _check_users_page(self):
        self.driver.get(f"{BASE_URL}/users/")
        self.driver.find_element(By.TAG_NAME, "table")
    def _check_finance_page(self):
        self.driver.get(f"{BASE_URL}/finance/transactions/")
        self.driver.find_element(By.TAG_NAME, "table")
    def _create_course(self):
        self.driver.get(f"{BASE_URL}/edu/courses/add/")
        self.driver.find_element(By.NAME, "name").send_keys("Test Robust Kurs")
        self.driver.find_element(By.NAME, "price").send_keys("500000")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        if "Test Robust Kurs" not in self.driver.page_source:
            raise Exception("Kurs ro'yxatda ko'rinmadi")
    def _check_dark_mode(self):
        try:
            btn = self.driver.find_element(By.ID, "theme-toggle")
            btn.click()
        except NoSuchElementException:
            self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleTheme')]").click()
    def run(self):
        try:
            self._login()
            self.log_success("Tizimga kirish")
        except Exception as e:
            self.log_fail("Tizimga kirish (Critical)", e)
            self.driver.quit()
            return
        steps = [
            ("Dashboard sahifasi", self._check_dashboard),
            ("Foydalanuvchilar sahifasi", self._check_users_page),
            ("Moliya sahifasi", self._check_finance_page),
            ("Kurs yaratish funksiyasi", self._create_course),
            ("Dark Mode tugmasi", self._check_dark_mode),
        ]
        for desc, func in steps:
            self.safe_action(desc, func)
        print(f"\n{Fore.CYAN}📊 HISOBOT:{Style.RESET_ALL}")
        print(f"Muvaffaqiyatli: {self.success_count}")
        print(f"Xatolar: {len(self.errors)}")
        if self.errors:
            print(f"{Fore.RED}⚠️ TUZATISH KERAK:{Style.RESET_ALL}")
            for err in self.errors:
                print(f" - {err}")
        else:
            print(f"{Fore.GREEN}🎉 AJOYIB! TIZIM BARQAROR ISHLAYAPTI.{Style.RESET_ALL}")
        self.driver.quit()
if __name__ == "__main__":
    tester = RobustTester()
    tester.run()

--- export_project.py ---
import os
import re
OUTPUT_FILE = "project_context_ultra.md"
IGNORE_DIRS = {
    'venv', '.venv', 'env', '.git', '.idea', '.vscode', '__pycache__',
    'migrations', 'media', 'static_root', 'staticfiles', 'node_modules', 'locale'
}
IGNORE_FILES = {
    'db.sqlite3', 'package-lock.json', 'yarn.lock', '.DS_Store',
    'poetry.lock', 'Pipfile.lock', 'manage.py', 'LICENSE', 'README.md'
}
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js'}
def remove_comments_and_docs(source):
    pattern = r"(\"\"\"[\s\S]*?\"\"\")|(\'\'\'[\s\S]*?\'\'\')"
    source = re.sub(pattern, "", source)
    source = re.sub(r"
    lines = [line.rstrip() for line in source.splitlines() if line.strip()]
    return "\n".join(lines)
def minify_html(content):
    content = re.sub(r"<!--[\s\S]*?-->", "", content)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return "\n".join(lines)
def is_boilerplate(filename, content):
    if not content.strip():
        return True
    if filename == "apps.py" and "AppConfig" in content and len(content) < 150:
        return True
    if filename == "tests.py" and len(content) < 100:
        return True
    return False
def generate_tree(root_dir):
    tree_str = "
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(root_dir, '').count(os.sep)
        indent = '  ' * level
        folder = os.path.basename(root)
        if level == 0: folder = "."
        tree_str += f"{indent}{folder}/\n"
        for f in files:
            if f.endswith(tuple(ALLOWED_EXTENSIONS)) and f not in IGNORE_FILES:
                tree_str += f"{indent}  {f}\n"
    tree_str += "\n"
    return tree_str
def main():
    root_dir = os.getcwd()
    print("🚀 Ultra-Optimallashtirish boshlandi...")
    total_files = 0
    ignored_count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("CONTEXT: Django Project. Comments removed for brevity. Interpret code logic.\n\n")
        outfile.write(generate_tree(root_dir))
        outfile.write("
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in ALLOWED_EXTENSIONS and file not in IGNORE_FILES and file != "export_ultra.py":
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            raw_content = f.read()
                        if ext == '.py':
                            clean_content = remove_comments_and_docs(raw_content)
                        else:
                            clean_content = minify_html(raw_content)
                        if is_boilerplate(file, clean_content):
                            ignored_count += 1
                            continue
                        outfile.write(f"--- {rel_path} ---\n")
                        outfile.write(clean_content)
                        outfile.write("\n\n")
                        total_files += 1
                        print(f"📦 {rel_path}")
                    except Exception as e:
                        print(f"❌ Xato: {rel_path}")
    print(f"\n✅ TAYYOR! {total_files} ta fayl yozildi. {ignored_count} ta keraksiz fayl tashlab ketildi.")
    print(f"📁 Natija: {OUTPUT_FILE}")
if __name__ == "__main__":
    main()

--- reset_db.py ---
import os
import shutil
from pathlib import Path
BASE_DIR = Path(__file__).parent
def clean_project():
    print("🧹 Loyiha tozalanmoqda...")
    db_path = BASE_DIR / "db.sqlite3"
    if db_path.exists():
        os.remove(db_path)
        print("✅ db.sqlite3 o'chirildi.")
    else:
        print("ℹ️  db.sqlite3 topilmadi (bu yaxshi).")
    apps_dir = BASE_DIR / "apps"
    if apps_dir.exists():
        for app_dir in apps_dir.iterdir():
            migration_dir = app_dir / "migrations"
            if migration_dir.exists() and migration_dir.is_dir():
                for file in migration_dir.iterdir():
                    if file.name != "__init__.py" and file.name != "__pycache__":
                        if file.is_file():
                            os.remove(file)
                        elif file.is_dir():
                            shutil.rmtree(file)
                print(f"✅ {app_dir.name} migratsiyalari tozalandi.")
    print("\n✨ TOZALASH TUGADI! Endi quyidagi buyruqlarni bering:")
    print("1. python manage.py makemigrations core users organizations crm education finance operations automation")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
if __name__ == "__main__":
    clean_project()

--- setup_initial_data.py ---
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from apps.organizations.models import Organization, Branch
from apps.users.models import User
def setup():
    print("Setting up initial data...")
    if not Organization.objects.exists():
        org = Organization.objects.create(
            name="Smart Edu Center",
            subdomain="smartedu",
            config={"theme": "light"}
        )
        print(f"Created organization: {org.name}")
    else:
        org = Organization.objects.first()
        print(f"Using existing organization: {org.name}")
    if not Branch.objects.exists():
        branch = Branch.objects.create(
            organization=org,
            name="Main Branch",
            address="Tashkent City",
            phone="+998901234567"
        )
        print(f"Created branch: {branch.name}")
    else:
        branch = Branch.objects.first()
        print(f"Using existing branch: {branch.name}")
    if not User.objects.filter(role='super_admin').exists():
        admin_password = "admin"
        admin = User.objects.create_superuser(
            phone="998900000000",
            password=admin_password,
            first_name="Super",
            last_name="Admin",
            role="super_admin",
            organization=org,
            branch=branch
        )
        print(f"Created Super Admin user.")
        print(f"Phone: 998900000000")
        print(f"Password: {admin_password}")
    else:
        print("Super Admin already exists.")
        print("Phone: 998900000000")
        print("Password: admin")
if __name__ == "__main__":
    setup()

--- apps\api\serializers.py ---
from rest_framework import serializers
from apps.users.models import User
from apps.finance.models import Transaction
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'balance', 'avatar']
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

--- apps\api\urls.py ---
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TransactionViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'transactions', TransactionViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

--- apps\api\views.py ---
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, TransactionSerializer
from apps.users.models import User
from apps.finance.models import Transaction
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return User.objects.all()
        return User.objects.filter(organization=user.organization)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            organization=self.request.user.organization,
            status='pending',
            receipt_verified=False
        )

--- apps\automation\apps.py ---
from django.apps import AppConfig
class AutomationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.automation'
    verbose_name = "Avtomatizatsiya"
    def ready(self):
        import apps.automation.signals

--- apps\automation\models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class NotificationTemplate(TenantAwareModel):
    TYPE_CHOICES = (
        ('sms', 'SMS'),
        ('telegram', 'Telegram'),
        ('system', 'Tizim Xabari'),
    )
    title = models.CharField(max_length=100, verbose_name="Shablon nomi")
    body = models.TextField(verbose_name="Xabar matni")
    code = models.CharField(max_length=50, unique=True, verbose_name="Kod (Foydalanish uchun)")
    message_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    def __str__(self):
        return f"{self.title} ({self.code})"
    class Meta:
        db_table = 'notification_templates'
        verbose_name = "Xabar Shabloni"
        verbose_name_plural = "Xabar Shablonlari"
class NotificationLog(TenantAwareModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Qabul qiluvchi")
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(verbose_name="Yuborilgan xabar")
    message_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='sent', choices=(
        ('sent', 'Yuborildi'),
        ('failed', 'Xatolik'),
        ('read', 'O\'qildi')
    ))
    def __str__(self):
        return f"{self.recipient} - {self.message[:30]}"
    class Meta:
        db_table = 'notification_logs'
        ordering = ['-created_at']

--- apps\automation\services.py ---
from django.conf import settings
from .models import NotificationTemplate, NotificationLog
from apps.users.models import User
import logging
logger = logging.getLogger(__name__)
def send_notification(user: User, template_code: str, context: dict = None):
    if context is None:
        context = {}
    context.update({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
    })
    try:
        template = NotificationTemplate.objects.filter(code=template_code, is_deleted=False).first()
        if not template:
            logger.warning(f"Notification template not found: {template_code}")
            return False
        try:
            message_body = template.body.format(**context)
        except KeyError as e:
            logger.error(f"Missing context key for template {template_code}: {e}")
            message_body = template.body
        if template.message_type == 'telegram' and settings.TELEGRAM_BOT_TOKEN:
            try:
                import telebot
                bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
                if user.telegram_id:
                    bot.send_message(user.telegram_id, message_body, parse_mode='HTML')
                    status = 'sent'
                else:
                    logger.warning(f"User {user} has no telegram_id")
                    status = 'failed'
            except Exception as e:
                logger.error(f"Telegram error: {e}")
                status = 'failed'
        else:
             status = 'sent'
        NotificationLog.objects.create(
            organization=user.organization,
            recipient=user,
            template=template,
            message=message_body,
            message_type=template.message_type,
            status=status
        )
        print(f"NOTIFICATION SENT [{template.message_type}] to {user.phone}: {message_body}")
        return True
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False

--- apps\automation\signals.py ---
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.operations.models import Attendance
from apps.finance.models import Transaction
from apps.automation.services import send_notification
@receiver(post_save, sender=Attendance)
def attendance_notification(sender, instance, created, **kwargs):
    if instance.status == 'absent':
        student = instance.student
        parents = student.parent_relations.all()
        for relation in parents:
            parent = relation.parent
            send_notification(
                user=parent,
                template_code='ATTENDANCE_ABSENT',
                context={
                    'parent_name': parent.first_name,
                    'student_name': student.full_name,
                    'date': instance.lesson.date,
                    'group': instance.lesson.group.name
                }
            )
@receiver(post_save, sender=Transaction)
def payment_notification(sender, instance, created, **kwargs):
    if instance.transaction_type == 'income' and instance.status == 'confirmed':
        student = instance.student
        if not student:
            return
        send_notification(
            user=student,
            template_code='PAYMENT_RECEIVED',
            context={
                'name': student.first_name,
                'amount': instance.amount,
                'date': instance.created_at.strftime('%d.%m.%Y'),
                'balance': student.balance
            }
        )
        parents = student.parent_relations.all()
        for relation in parents:
            parent = relation.parent
            send_notification(
                user=parent,
                template_code='PAYMENT_RECEIVED_PARENT',
                context={
                    'parent_name': parent.first_name,
                    'student_name': student.full_name,
                    'amount': instance.amount,
                    'date': instance.created_at.strftime('%d.%m.%Y'),
                     'balance': student.balance
                }
            )

--- apps\automation\urls.py ---
from django.urls import path
from . import views
app_name = 'automation'
urlpatterns = [
    path('templates/', views.template_list, name='template_list'),
    path('templates/add/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
]

--- apps\automation\views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.core.audit import log_user_action
from .models import NotificationTemplate
from django import forms
class NotificationTemplateForm(forms.ModelForm):
    class Meta:
        model = NotificationTemplate
        fields = ['title', 'code', 'message_type', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'message_type': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'body': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300', 'rows': 5}),
        }
@login_required
def template_list(request):
    templates = NotificationTemplate.objects.filter(is_deleted=False)
    if request.user.role != 'super_admin' and request.user.organization:
        templates = templates.filter(organization=request.user.organization)
    return render(request, 'automation/template_list.html', {'templates': templates})
@login_required
def template_create(request):
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.organization = request.user.organization
            template.save()
            log_user_action(request.user, 'CREATE', 'NotificationTemplate', template.id, str(template), request=request)
            messages.success(request, "Shablon yaratildi!")
            return redirect('automation:template_list')
    else:
        form = NotificationTemplateForm()
    return render(request, 'automation/template_form.html', {'form': form, 'title': "Yangi Shablon"})
@login_required
def template_edit(request, pk):
    template = get_object_or_404(NotificationTemplate, pk=pk)
    if request.user.role != 'super_admin' and template.organization != request.user.organization:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('automation:template_list')
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'NotificationTemplate', template.id, str(template), request=request)
            messages.success(request, "Shablon yangilandi!")
            return redirect('automation:template_list')
    else:
        form = NotificationTemplateForm(instance=template)
    return render(request, 'automation/template_form.html', {'form': form, 'title': "Shablonni tahrirlash"})
@login_required
def template_delete(request, pk):
    template = get_object_or_404(NotificationTemplate, pk=pk)
    if request.method == 'POST':
        template.is_deleted = True
        template.save()
        log_user_action(request.user, 'DELETE', 'NotificationTemplate', template.id, str(template), request=request)
        messages.success(request, "Shablon o'chirildi")
    return redirect('automation:template_list')

--- apps\automation\management\commands\runbot.py ---
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.users.models import User
import telebot
import logging
try:
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode='HTML')
except Exception:
    bot = None
    print("TELEGRAM_BOT_TOKEN topilmadi yoki xato.")
logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish'
    def handle(self, *args, **options):
        if not bot:
            self.stdout.write(self.style.ERROR("Bot tokeni topilmadi!"))
            return
        self.stdout.write(self.style.SUCCESS("Bot ishga tushdi..."))
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            chat_id = message.chat.id
            username = message.from_user.username
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button = telebot.types.KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)
            keyboard.add(button)
            bot.send_message(
                chat_id,
                "Assalomu alaykum! Smart Edu tizimiga xush kelibsiz.\nIltimos, shaxsingizni tasdiqlash uchun telefon raqamingizni yuboring.",
                reply_markup=keyboard
            )
        @bot.message_handler(content_types=['contact'])
        def handle_contact(message):
            if message.contact is not None:
                phone = message.contact.phone_number
                chat_id = message.chat.id
                if phone.startswith('+'):
                    phone = phone[1:]
                try:
                    user = User.objects.get(phone=phone)
                    user.telegram_id = chat_id
                    user.save()
                    bot.send_message(chat_id, f"Rahmat, {user.first_name}! Siz tizimga muvaffaqiyatli ulandingiz. Endi bildirishnomalarni shu yerda olasiz.")
                    self.stdout.write(self.style.SUCCESS(f"User linked: {user.phone} -> {chat_id}"))
                except User.DoesNotExist:
                    bot.send_message(chat_id, "Kechirasiz, bu raqam tizimda topilmadi. Administratorga murojaat qiling.")
                    self.stdout.write(self.style.WARNING(f"User not found for phone: {phone}"))
        bot.infinity_polling()

--- apps\automation\management\commands\setup_templates.py ---
from django.core.management.base import BaseCommand
from apps.automation.models import NotificationTemplate
from apps.organizations.models import Organization
class Command(BaseCommand):
    help = 'Create default notification templates'
    def handle(self, *args, **options):
        orgs = Organization.objects.all()
        if not orgs.exists():
            self.stdout.write(self.style.WARNING("Tashkilot topilmadi"))
            return
        templates_data = [
            {
                'title': "Darsga kelmaganlik",
                'code': "ATTENDANCE_ABSENT",
                'message_type': "telegram",
                'body': "Hurmatli <b>{parent_name}</b>,\n\nFarzandingiz <b>{student_name}</b> bugungi {date} sanadagi <b>{group}</b> darsiga qatnashmadi.\n\nIltimos nazorat qiling."
            },
            {
                'title': "To'lov qabul qilindi (Student)",
                'code': "PAYMENT_RECEIVED",
                'message_type': "telegram",
                'body': "Assalomu alaykum <b>{name}</b>!\n\nSizning {amount} UZS miqdoridagi to'lovingiz qabul qilindi.\n\n📅 Sana: {date}\n💰 Hozirgi balans: {balance} UZS"
            },
            {
                'title': "To'lov qabul qilindi (Parent)",
                'code': "PAYMENT_RECEIVED_PARENT",
                'message_type': "telegram",
                'body': "Hurmatli <b>{parent_name}</b>,\n\nFarzandingiz <b>{student_name}</b> uchun {amount} UZS to'lov muvaffaqiyatli qabul qilindi.\n\n📅 Sana: {date}\n💰 Hozirgi balans: {balance} UZS"
            }
        ]
        for org in orgs:
            for data in templates_data:
                obj, created = NotificationTemplate.objects.get_or_create(
                    organization=org,
                    code=data['code'],
                    defaults={
                        'title': data['title'],
                        'message_type': data['message_type'],
                        'body': data['body']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created template: {data['code']} for {org.name}"))
                else:
                    self.stdout.write(f"Template already exists: {data['code']}")

--- apps\core\audit.py ---
from functools import wraps
from .models import AuditLog
class AuditMixin:
    def get_audit_object_repr(self, obj):
        return str(obj)
    def log_create(self, obj, request=None):
        AuditLog.log(
            user=request.user if request else None,
            action='CREATE',
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            object_repr=self.get_audit_object_repr(obj),
            request=request
        )
    def log_update(self, obj, changes, request=None):
        AuditLog.log(
            user=request.user if request else None,
            action='UPDATE',
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            object_repr=self.get_audit_object_repr(obj),
            changes=changes,
            request=request
        )
    def log_delete(self, obj, request=None):
        AuditLog.log(
            user=request.user if request else None,
            action='DELETE',
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            object_repr=self.get_audit_object_repr(obj),
            request=request
        )
def get_model_changes(instance, old_instance):
    changes = {}
    for field in instance._meta.fields:
        field_name = field.name
        if 'password' in field_name.lower() or 'secret' in field_name.lower():
            continue
        old_value = getattr(old_instance, field_name, None)
        new_value = getattr(instance, field_name, None)
        try:
            if old_value != new_value:
                changes[field_name] = {
                    'old': str(old_value) if old_value else None,
                    'new': str(new_value) if new_value else None
                }
        except Exception:
            pass
    return changes
def audit_action(action_type):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            return response
        return wrapper
    return decorator
def log_user_action(user, action, model_name, object_id=None, object_repr='', changes=None, request=None):
    return AuditLog.log(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        changes=changes,
        request=request
    )

--- apps\core\context_processors.py ---
def tenant_context(request):
    return {
        'organization': request.organization
    }

--- apps\core\dashboards.py ---
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, ParentStudent
from apps.organizations.models import Organization, Branch
from apps.crm.models import Lead, Stage
from apps.education.models import Course, Group, GroupStudent
from apps.operations.models import Lesson, Attendance
from apps.finance.models import Transaction, Account
def get_date_range(days=30):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date
@login_required
def role_based_dashboard(request):
    user = request.user
    role = user.role
    if role == 'super_admin':
        return super_admin_dashboard(request)
    elif role in ['owner', 'admin']:
        return admin_dashboard(request)
    elif role == 'teacher':
        return teacher_dashboard(request)
    elif role == 'student':
        return student_dashboard(request)
    elif role == 'parent':
        return parent_dashboard(request)
    else:
        return staff_dashboard(request)
@login_required
def super_admin_dashboard(request):
    from django.db.models import F
    from apps.finance.inventory import Supply
    today = timezone.now().date()
    period = request.GET.get('period', 'monthly')
    if period == 'weekly':
        start_date, end_date = get_date_range(7)
        period_label = "Haftalik"
    else:
        start_date, end_date = get_date_range(30)
        period_label = "Oylik"
    total_orgs = Organization.objects.filter(is_deleted=False).count()
    active_orgs = Organization.objects.filter(is_deleted=False, is_active=True).count()
    total_users = User.objects.filter(is_active=True).count()
    users_by_role = User.objects.filter(is_active=True).values('role').annotate(count=Count('id'))
    users_by_role_dict = {item['role']: item['count'] for item in users_by_role}
    total_students = users_by_role_dict.get('student', 0)
    active_students = User.objects.filter(role='student', is_active=True, is_deleted=False).count()
    frozen_students = GroupStudent.objects.filter(status='frozen').values('student').distinct().count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_leads_today = Lead.objects.filter(created_at__date=today).count()
    today_income = Transaction.objects.filter(
        transaction_type='income',
        status='confirmed',
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    today_expense = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed',
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    period_income = Transaction.objects.filter(
        transaction_type='income',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    period_expense = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    net_profit = period_income - period_expense
    daily_expenses = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed',
        created_at__date=today
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    debtors = User.objects.filter(role='student', balance__lt=0, is_active=True)
    total_debt = abs(debtors.aggregate(total=Sum('balance'))['total'] or 0)
    debtors_count = debtors.count()
    today_birthdays = User.objects.filter(
        is_active=True,
        birth_date__month=today.month,
        birth_date__day=today.day
    ).select_related('organization')[:10]
    today_lessons = Lesson.objects.filter(date=today)
    total_today_lessons = today_lessons.count()
    finished_lessons = today_lessons.filter(status='finished').count()
    today_attendance = Attendance.objects.filter(lesson__date=today)
    total_attendances = today_attendance.count()
    present_count = today_attendance.filter(status='present').count()
    attendance_rate = (present_count / total_attendances * 100) if total_attendances > 0 else 0
    total_groups = Group.objects.filter(is_deleted=False).count()
    active_groups = Group.objects.filter(status='active', is_deleted=False).count()
    recent_orgs = Organization.objects.filter(is_deleted=False).order_by('-created_at')[:5]
    recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:10]
    recent_transactions = Transaction.objects.filter(status='confirmed').order_by('-created_at')[:5]
    pending_payments = Transaction.objects.filter(
        status='pending',
        transaction_type='income'
    ).count()
    pending_receipts = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).count()
    pending_receipts_sum = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).aggregate(total=Sum('amount'))['total'] or 0
    pending_receipts_list = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).select_related('student', 'created_by').order_by('-created_at')[:5]
    low_stock_items = Supply.objects.filter(
        is_deleted=False,
        quantity__lte=F('min_quantity')
    )[:10]
    low_stock_count = Supply.objects.filter(
        is_deleted=False,
        quantity__lte=F('min_quantity')
    ).count()
    context = {
        'total_orgs': total_orgs,
        'active_orgs': active_orgs,
        'total_users': total_users,
        'users_by_role': users_by_role_dict,
        'total_students': total_students,
        'active_students': active_students,
        'frozen_students': frozen_students,
        'new_users_today': new_users_today,
        'new_leads_today': new_leads_today,
        'period': period,
        'period_label': period_label,
        'today_income': today_income,
        'today_expense': today_expense,
        'period_income': period_income,
        'period_expense': period_expense,
        'net_profit': net_profit,
        'daily_expenses': daily_expenses,
        'total_debt': total_debt,
        'debtors_count': debtors_count,
        'today_birthdays': today_birthdays,
        'total_today_lessons': total_today_lessons,
        'finished_lessons': finished_lessons,
        'attendance_rate': round(attendance_rate, 1),
        'total_groups': total_groups,
        'active_groups': active_groups,
        'recent_orgs': recent_orgs,
        'recent_users': recent_users,
        'recent_transactions': recent_transactions,
        'pending_payments': pending_payments,
        'pending_receipts': pending_receipts,
        'pending_receipts_sum': pending_receipts_sum,
        'pending_receipts_list': pending_receipts_list,
        'low_stock_items': low_stock_items,
        'low_stock_count': low_stock_count,
        'today': today,
    }
    return render(request, 'dashboards/super_admin.html', context)
@login_required
def admin_dashboard(request):
    org = request.user.organization
    total_students = User.objects.filter(
        organization=org, role='student', is_active=True, is_deleted=False
    ).count()
    total_teachers = User.objects.filter(
        organization=org, role='teacher', is_active=True, is_deleted=False
    ).count()
    active_groups = Group.objects.filter(
        organization=org, status='active', is_deleted=False
    ).count()
    total_leads = Lead.objects.filter(organization=org, is_deleted=False).count()
    new_leads = Lead.objects.filter(
        organization=org,
        is_deleted=False,
        created_at__date=timezone.now().date()
    ).count()
    start_date, end_date = get_date_range(30)
    monthly_income = Transaction.objects.filter(
        organization=org,
        transaction_type='income',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_debt = User.objects.filter(
        organization=org, role='student', balance__lt=0
    ).aggregate(total=Sum('balance'))['total'] or 0
    today_lessons = Lesson.objects.filter(
        organization=org,
        date=timezone.now().date()
    ).select_related('group', 'teacher', 'room').order_by('start_time')[:10]
    recent_leads = Lead.objects.filter(
        organization=org, is_deleted=False
    ).select_related('source', 'stage').order_by('-created_at')[:5]
    stages = Stage.objects.filter(organization=org).annotate(
        lead_count=Count('leads', filter=Q(leads__is_deleted=False))
    ).order_by('order')
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'active_groups': active_groups,
        'total_leads': total_leads,
        'new_leads': new_leads,
        'monthly_income': monthly_income,
        'total_debt': abs(total_debt),
        'today_lessons': today_lessons,
        'recent_leads': recent_leads,
        'stages': stages,
    }
    return render(request, 'dashboards/admin.html', context)
@login_required
def teacher_dashboard(request):
    from django.db.models import Avg
    teacher = request.user
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    my_groups = Group.objects.filter(
        teacher=teacher,
        status__in=['active', 'pending'],
        is_deleted=False
    ).select_related('course', 'room').annotate(
        student_count=Count('students', filter=Q(students__status='active'))
    )
    today_lessons = Lesson.objects.filter(
        teacher=teacher,
        date=today
    ).select_related('group', 'room').order_by('start_time')
    upcoming_lessons = Lesson.objects.filter(
        teacher=teacher,
        date__gt=today,
        date__lte=today + timedelta(days=5)
    ).select_related('group', 'room').order_by('date', 'start_time')[:10]
    pending_attendance = Lesson.objects.filter(
        teacher=teacher,
        date__lte=today,
        status='scheduled'
    ).select_related('group').order_by('-date')[:5]
    total_students = GroupStudent.objects.filter(
        group__teacher=teacher,
        group__status='active',
        status='active'
    ).count()
    monthly_lessons = Lesson.objects.filter(
        teacher=teacher,
        date__gte=start_of_month,
        date__lte=today
    )
    total_monthly_lessons = monthly_lessons.count()
    completed_lessons = monthly_lessons.filter(status='finished').count()
    lesson_completion_rate = (completed_lessons / total_monthly_lessons * 100) if total_monthly_lessons > 0 else 0
    my_lesson_ids = monthly_lessons.values_list('id', flat=True)
    monthly_attendance = Attendance.objects.filter(lesson_id__in=my_lesson_ids)
    total_attendance_records = monthly_attendance.count()
    present_records = monthly_attendance.filter(status='present').count()
    student_attendance_rate = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0
    avg_grade_given = monthly_attendance.filter(
        grade__isnull=False
    ).aggregate(avg=Avg('grade'))['avg'] or 0
    total_xp_given = monthly_attendance.aggregate(
        total=Sum('xp_points')
    )['total'] or 0
    context = {
        'my_groups': my_groups,
        'today_lessons': today_lessons,
        'upcoming_lessons': upcoming_lessons,
        'pending_attendance': pending_attendance,
        'total_students': total_students,
        'today': today,
        'total_monthly_lessons': total_monthly_lessons,
        'completed_lessons': completed_lessons,
        'lesson_completion_rate': round(lesson_completion_rate, 1),
        'student_attendance_rate': round(student_attendance_rate, 1),
        'avg_grade_given': round(avg_grade_given, 1),
        'total_xp_given': total_xp_given,
    }
    return render(request, 'dashboards/teacher.html', context)
@login_required
def student_dashboard(request):
    from apps.operations.shop import ShopItem
    student = request.user
    today = timezone.now().date()
    my_enrollments = GroupStudent.objects.filter(
        student=student,
        status='active'
    ).select_related('group', 'group__course', 'group__teacher', 'group__room')
    my_groups = [e.group for e in my_enrollments]
    today_lessons = Lesson.objects.filter(
        group__in=my_groups,
        date=today
    ).select_related('group', 'teacher', 'room').order_by('start_time')
    upcoming_lessons = Lesson.objects.filter(
        group__in=my_groups,
        date__gt=today
    ).select_related('group', 'teacher', 'room').order_by('date', 'start_time')[:10]
    my_attendance = Attendance.objects.filter(
        student=student
    ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:20]
    total_lessons = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='present').count()
    attendance_rate = (present_count / total_lessons * 100) if total_lessons > 0 else 0
    grades = Attendance.objects.filter(
        student=student,
        grade__isnull=False
    ).values_list('grade', flat=True)
    avg_grade = sum(grades) / len(grades) if grades else 0
    total_xp = Attendance.objects.filter(student=student).aggregate(
        total=Sum('xp_points')
    )['total'] or 0
    coin_balance = student.profile_data.get('xp', total_xp) if hasattr(student, 'profile_data') and student.profile_data else total_xp
    balance = student.balance
    payments = Transaction.objects.filter(
        student=student
    ).order_by('-created_at')[:10]
    grade_history = Attendance.objects.filter(
        student=student,
        grade__isnull=False
    ).select_related('lesson').order_by('lesson__date')
    grade_history = list(grade_history)[-10:]
    chart_labels = [att.lesson.date.strftime('%d.%m') for att in grade_history]
    chart_data = [att.grade for att in grade_history]
    org = student.organization
    leaderboard = User.objects.filter(
        role='student',
        organization=org,
        is_active=True,
        is_deleted=False
    ).annotate(
        xp_total=Sum('attendances__xp_points')
    ).exclude(xp_total__isnull=True).order_by('-xp_total')[:10]
    student_rank = 0
    for i, s in enumerate(leaderboard, 1):
        if s.id == student.id:
            student_rank = i
            break
    shop_items_count = ShopItem.objects.filter(
        organization=org,
        is_active=True,
        is_deleted=False
    ).count() if org else 0
    context = {
        'my_enrollments': my_enrollments,
        'today_lessons': today_lessons,
        'upcoming_lessons': upcoming_lessons,
        'my_attendance': my_attendance,
        'attendance_rate': round(attendance_rate, 1),
        'avg_grade': round(avg_grade, 1),
        'total_xp': total_xp,
        'coin_balance': coin_balance,
        'balance': balance,
        'payments': payments,
        'today': today,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'leaderboard': leaderboard,
        'student_rank': student_rank,
        'shop_items_count': shop_items_count,
    }
    return render(request, 'dashboards/student.html', context)
@login_required
def parent_dashboard(request):
    parent = request.user
    today = timezone.now().date()
    children_relations = ParentStudent.objects.filter(
        parent=parent
    ).select_related('student')
    children_data = []
    for relation in children_relations:
        child = relation.student
        enrollments = GroupStudent.objects.filter(
            student=child,
            status='active'
        ).select_related('group', 'group__course', 'group__teacher')
        total_att = Attendance.objects.filter(student=child).count()
        present = Attendance.objects.filter(student=child, status='present').count()
        att_rate = (present / total_att * 100) if total_att > 0 else 0
        grades = Attendance.objects.filter(
            student=child, grade__isnull=False
        ).values_list('grade', flat=True)
        avg_grade = sum(grades) / len(grades) if grades else 0
        recent_attendance = Attendance.objects.filter(
            student=child
        ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:5]
        children_data.append({
            'child': child,
            'relation_type': relation.get_relation_type_display(),
            'enrollments': enrollments,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
            'balance': child.balance,
            'has_debt': child.balance < 0,
            'xp': Attendance.objects.filter(student=child).aggregate(total=Sum('xp_points'))['total'] or 0,
            'recent_attendance': recent_attendance,
        })
    total_debt = sum(abs(d['balance']) for d in children_data if d['has_debt'])
    has_any_debt = any(d['has_debt'] for d in children_data)
    context = {
        'children_data': children_data,
        'today': today,
        'total_debt': total_debt,
        'has_any_debt': has_any_debt,
    }
    return render(request, 'dashboards/parent.html', context)
@login_required
def staff_dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboards/staff.html', context)

--- apps\core\export_views.py ---
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import date, timedelta
from apps.core.services import export_transactions_csv, get_financial_chart_data
@login_required
def export_transactions(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if start_date:
        start_date = date.fromisoformat(start_date)
    else:
        start_date = date.today().replace(day=1)
    if end_date:
        end_date = date.fromisoformat(end_date)
    else:
        end_date = date.today()
    csv_content = export_transactions_csv(
        request.user.organization,
        start_date,
        end_date
    )
    response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="transactions_{start_date}_{end_date}.csv"'
    return response
@login_required
def api_chart_data(request):
    import json
    from django.http import JsonResponse
    days = int(request.GET.get('days', 30))
    chart_data = get_financial_chart_data(request.user.organization, days)
    return JsonResponse(chart_data)
@login_required
def global_search(request):
    from django.db.models import Q
    from apps.users.models import User
    from apps.crm.models import Lead
    from apps.education.models import Group
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return render(request, 'components/search_results.html', {'results': []})
    org = request.user.organization
    users = User.objects.filter(
        organization=org
    ).filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(phone__icontains=query)
    )[:5]
    leads = Lead.objects.filter(
        organization=org
    ).filter(
        Q(name__icontains=query) |
        Q(phone__icontains=query)
    )[:5]
    groups = Group.objects.filter(
        organization=org,
        name__icontains=query
    )[:5]
    results = []
    for user in users:
        results.append({
            'type': 'user',
            'icon': 'ph-user',
            'title': user.full_name,
            'subtitle': f"{user.get_role_display()} • {user.phone}",
            'url': f"/users/{user.id}/",
        })
    for lead in leads:
        results.append({
            'type': 'lead',
            'icon': 'ph-user-plus',
            'title': lead.name,
            'subtitle': f"Lead • {lead.phone}",
            'url': f"/crm/leads/{lead.id}/",
        })
    for group in groups:
        results.append({
            'type': 'group',
            'icon': 'ph-users-three',
            'title': group.name,
            'subtitle': f"Guruh • {group.get_status_display()}",
            'url': f"/education/groups/{group.id}/",
        })
    return render(request, 'components/search_results.html', {'results': results, 'query': query})

--- apps\core\history_views.py ---
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from apps.core.models import AuditLog
from apps.users.models import User
@login_required
def history_list(request):
    logs = AuditLog.objects.select_related('user', 'organization').order_by('-created_at')
    if request.user.role != 'super_admin' and request.user.organization:
        logs = logs.filter(organization=request.user.organization)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(created_at__date__gte=date_from)
    if date_to:
        logs = logs.filter(created_at__date__lte=date_to)
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    model_name = request.GET.get('model')
    if model_name:
        logs = logs.filter(model_name__icontains=model_name)
    search = request.GET.get('q')
    if search:
        logs = logs.filter(
            Q(object_repr__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(model_name__icontains=search)
        )
    paginator = Paginator(logs, 50)
    page = request.GET.get('page', 1)
    logs_page = paginator.get_page(page)
    users_with_logs = User.objects.filter(
        audit_logs__isnull=False
    ).distinct().order_by('first_name')
    model_names = AuditLog.objects.values_list('model_name', flat=True).distinct()
    context = {
        'logs': logs_page,
        'users': users_with_logs,
        'model_names': set(model_names),
        'action_choices': AuditLog.ACTION_CHOICES,
        'current_action': action,
        'current_user': user_id,
        'current_model': model_name,
        'current_search': search,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'core/history.html', context)
@login_required
def history_detail(request, log_id):
    log = get_object_or_404(AuditLog, id=log_id)
    if request.user.role != 'super_admin':
        if log.organization != request.user.organization:
            return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)
    return render(request, 'core/history_detail.html', {'log': log})

--- apps\core\middleware.py ---
import threading
from django.utils.deprecation import MiddlewareMixin
from django.apps import apps
from django.conf import settings
_thread_locals = threading.local()
def get_current_organization():
    return getattr(_thread_locals, 'organization', None)
class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]
        Organization = apps.get_model('organizations', 'Organization')
        request.organization = None
        if settings.DEBUG and (subdomain == 'localhost' or subdomain == '127'):
            if Organization.objects.exists():
                request.organization = Organization.objects.first()
            else:
                try:
                    from apps.users.models import User
                    owner = User.objects.filter(role='super_admin').first()
                    if not owner and User.objects.exists():
                        owner = User.objects.first()
                    request.organization = Organization.objects.create(
                        name="Smart Edu Test",
                        subdomain="test",
                        owner=owner
                    )
                    print("⚠️ TEST UCHUN TASHKILOT AVTOMATIK YARATILDI!")
                except Exception:
                    pass
        else:
            try:
                request.organization = Organization.objects.get(subdomain=subdomain, is_active=True)
            except Organization.DoesNotExist:
                pass
        _thread_locals.organization = request.organization

--- apps\core\models.py ---
import uuid
from django.db import models
from django.utils import timezone
from apps.core.middleware import get_current_organization
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")
    class Meta:
        abstract = True
class SoftDeleteModel(BaseModel):
    is_deleted = models.BooleanField(default=False, verbose_name="O'chirilganmi?")
    deleted_at = models.DateTimeField(null=True, blank=True)
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
    class Meta:
        abstract = True
class TenantAwareModel(SoftDeleteModel):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
        verbose_name="Tashkilot",
        null=True, blank=True
    )
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.organization_id:
            org = get_current_organization()
            if org:
                self.organization = org
        super().save(*args, **kwargs)
class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Yaratildi'),
        ('UPDATE', 'O\'zgartirildi'),
        ('DELETE', 'O\'chirildi'),
        ('LOGIN', 'Tizimga kirdi'),
        ('LOGOUT', 'Tizimdan chiqdi'),
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='audit_logs'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name="Kim bajardi"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Amal")
    model_name = models.CharField(max_length=100, verbose_name="Model nomi")
    object_id = models.IntegerField(null=True, blank=True, verbose_name="Obyekt ID")
    object_repr = models.CharField(max_length=255, blank=True, verbose_name="Obyekt nomi")
    changes = models.JSONField(default=dict, blank=True, verbose_name="O'zgarishlar")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Manzil")
    user_agent = models.CharField(max_length=500, blank=True, verbose_name="Brauzer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Loglar"
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
    @classmethod
    def log(cls, user, action, model_name, object_id=None, object_repr='', changes=None, request=None):
        log_entry = cls(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            object_repr=object_repr[:255] if object_repr else '',
            changes=changes or {},
        )
        if user and hasattr(user, 'organization'):
            log_entry.organization = user.organization
        if request and hasattr(request, 'organization') and request.organization:
            log_entry.organization = request.organization
        if request:
            log_entry.ip_address = cls.get_client_ip(request)
            log_entry.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        log_entry.save()
        return log_entry
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

--- apps\core\services.py ---
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
def calculate_student_stats(student):
    from apps.operations.models import Attendance, Lesson
    from apps.finance.models import Transaction
    from apps.education.models import GroupStudent
    attendances = Attendance.objects.filter(student=student)
    total_lessons = attendances.count()
    present_count = attendances.filter(status='present').count()
    late_count = attendances.filter(status='late').count()
    absent_count = attendances.filter(status='absent').count()
    attendance_rate = (present_count / total_lessons * 100) if total_lessons > 0 else 0
    grades = attendances.exclude(grade__isnull=True).values_list('grade', flat=True)
    avg_grade = sum(grades) / len(grades) if grades else 0
    xp = student.profile_data.get('xp', 0)
    active_groups = GroupStudent.objects.filter(student=student, status='active').count()
    payments = Transaction.objects.filter(
        student=student,
        transaction_type='income',
        status='confirmed'
    )
    total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    return {
        'total_lessons': total_lessons,
        'present_count': present_count,
        'late_count': late_count,
        'absent_count': absent_count,
        'attendance_rate': round(attendance_rate, 1),
        'avg_grade': round(avg_grade, 1),
        'xp': xp,
        'active_groups': active_groups,
        'total_paid': total_paid,
        'balance': student.balance,
    }
def calculate_teacher_stats(teacher, month=None):
    from apps.operations.models import Lesson, Attendance
    from apps.education.models import Group, GroupStudent
    if month is None:
        month = date.today().replace(day=1)
    next_month = (month.replace(day=28) + timedelta(days=4)).replace(day=1)
    groups = Group.objects.filter(teacher=teacher, status='active')
    lessons = Lesson.objects.filter(
        teacher=teacher,
        date__gte=month,
        date__lt=next_month
    )
    completed_lessons = lessons.filter(status='finished').count()
    scheduled_lessons = lessons.filter(status='scheduled').count()
    students_count = GroupStudent.objects.filter(
        group__teacher=teacher,
        group__status='active',
        status='active'
    ).values('student').distinct().count()
    attendances = Attendance.objects.filter(
        lesson__teacher=teacher,
        lesson__date__gte=month,
        lesson__date__lt=next_month
    )
    if attendances.exists():
        present = attendances.filter(status='present').count()
        attendance_rate = (present / attendances.count()) * 100
    else:
        attendance_rate = 0
    grades = attendances.exclude(grade__isnull=True).values_list('grade', flat=True)
    avg_grade = sum(grades) / len(grades) if grades else 0
    return {
        'groups_count': groups.count(),
        'students_count': students_count,
        'completed_lessons': completed_lessons,
        'scheduled_lessons': scheduled_lessons,
        'attendance_rate': round(attendance_rate, 1),
        'avg_grade': round(avg_grade, 1),
    }
def calculate_organization_stats(organization, period='month'):
    from apps.users.models import User
    from apps.crm.models import Lead
    from apps.education.models import Group, GroupStudent
    from apps.operations.models import Lesson
    from apps.finance.models import Transaction
    today = date.today()
    if period == 'today':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today.replace(day=1)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today - timedelta(days=30)
    students = User.objects.filter(organization=organization, role='student', is_active=True)
    teachers = User.objects.filter(organization=organization, role='teacher', is_active=True)
    active_groups = Group.objects.filter(organization=organization, status='active')
    leads = Lead.objects.filter(organization=organization, created_at__date__gte=start_date)
    won_leads = leads.filter(stage__stage_type='won')
    transactions = Transaction.objects.filter(
        organization=organization,
        created_at__date__gte=start_date,
        status='confirmed'
    )
    income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = transactions.filter(transaction_type__in=['expense', 'salary']).aggregate(Sum('amount'))['amount__sum'] or 0
    lessons_today = Lesson.objects.filter(
        organization=organization,
        date=today
    )
    return {
        'students_count': students.count(),
        'teachers_count': teachers.count(),
        'active_groups': active_groups.count(),
        'leads_count': leads.count(),
        'won_leads': won_leads.count(),
        'conversion_rate': round((won_leads.count() / leads.count() * 100) if leads.count() > 0 else 0, 1),
        'total_income': income,
        'total_expense': expense,
        'net_profit': income - expense,
        'lessons_today': lessons_today.count(),
        'lessons_scheduled': lessons_today.filter(status='scheduled').count(),
        'lessons_finished': lessons_today.filter(status='finished').count(),
    }
def get_financial_chart_data(organization, days=30):
    from apps.finance.models import Transaction
    from django.db.models.functions import TruncDate
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    transactions = Transaction.objects.filter(
        organization=organization,
        created_at__date__gte=start_date,
        status='confirmed'
    ).annotate(
        date_only=TruncDate('created_at')
    ).values('date_only', 'transaction_type').annotate(
        total=Sum('amount')
    ).order_by('date_only')
    dates = []
    income_data = []
    expense_data = []
    current = start_date
    while current <= end_date:
        dates.append(current.strftime('%d.%m'))
        day_income = sum(
            float(t['total']) for t in transactions
            if t['date_only'] == current and t['transaction_type'] == 'income'
        )
        day_expense = sum(
            float(t['total']) for t in transactions
            if t['date_only'] == current and t['transaction_type'] in ['expense', 'salary']
        )
        income_data.append(day_income)
        expense_data.append(day_expense)
        current += timedelta(days=1)
    return {
        'labels': dates,
        'income': income_data,
        'expense': expense_data,
    }
def get_lead_sources_chart(organization, days=30):
    from apps.crm.models import Lead
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    leads = Lead.objects.filter(
        organization=organization,
        created_at__date__gte=start_date
    ).values('source__name').annotate(
        count=Count('id')
    ).order_by('-count')
    return {
        'labels': [l['source__name'] or "Noma'lum" for l in leads],
        'data': [l['count'] for l in leads],
    }
def export_transactions_csv(organization, start_date, end_date):
    import csv
    from io import StringIO
    from apps.finance.models import Transaction
    transactions = Transaction.objects.filter(
        organization=organization,
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).select_related('account', 'category', 'student', 'staff', 'created_by').order_by('created_at')
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Sana', 'Vaqt', 'Turi', 'Kategoriya', 'Summa', 'Kassa',
        "O'quvchi", 'Xodim', 'Izoh', 'Holat', 'Kiritdi'
    ])
    for t in transactions:
        writer.writerow([
            t.created_at.strftime('%d.%m.%Y'),
            t.created_at.strftime('%H:%M'),
            t.get_transaction_type_display(),
            t.category.name if t.category else '',
            float(t.amount),
            t.account.name,
            t.student.full_name if t.student else '',
            t.staff.full_name if t.staff else '',
            t.description,
            t.get_status_display(),
            t.created_by.full_name if t.created_by else '',
        ])
    return output.getvalue()
def check_low_stock_supplies(organization):
    from apps.finance.inventory import Supply
    low_stock = Supply.objects.filter(
        organization=organization,
        quantity__lte=F('min_quantity')
    )
    return list(low_stock.values('id', 'name', 'quantity', 'min_quantity', 'unit'))
def calculate_group_profitability(group):
    from apps.education.models import GroupStudent
    from apps.finance.models import Transaction
    from apps.operations.models import Lesson
    students = GroupStudent.objects.filter(group=group).values_list('student_id', flat=True)
    income = Transaction.objects.filter(
        student_id__in=students,
        transaction_type='income',
        status='confirmed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    lessons = Lesson.objects.filter(group=group, status='finished').count()
    per_lesson_rate = 50000
    if group.teacher and group.teacher.profile_data:
        per_lesson_rate = group.teacher.profile_data.get('per_lesson_rate', 50000)
    teacher_cost = lessons * per_lesson_rate
    profit = float(income) - teacher_cost
    return {
        'total_income': income,
        'teacher_cost': teacher_cost,
        'lessons_count': lessons,
        'profit': profit,
        'profit_per_lesson': profit / lessons if lessons > 0 else 0,
    }

--- apps\core\tasks.py ---
from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import telebot
import os
@shared_task
def backup_and_report():
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M')
    backup_file = f"backup_{timestamp}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], stdout=f)
    if settings.TELEGRAM_BOT_TOKEN:
        try:
            bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
            print(f"Backup tayyor: {backup_file}")
        except Exception as e:
            print(f"Telegram error: {e}")
    return "Backup sent!"

--- apps\core\urls.py ---
from django.urls import path
from apps.core.history_views import history_list, history_detail
app_name = 'core'
urlpatterns = [
    path('history/', history_list, name='history_list'),
    path('history/<int:log_id>/', history_detail, name='history_detail'),
]

--- apps\core\views.py ---
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .dashboards import role_based_dashboard
@login_required
def dashboard_view(request):
    return role_based_dashboard(request)

--- apps\core\management\commands\audit_system.py ---
from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError
import os
class Command(BaseCommand):
    help = 'Scans project for URL and Template errors'
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting Deep System Audit...'))
        self.stdout.write('\n1. Checking Templates Syntax...')
        template_errors = 0
        from django.conf import settings
        template_dirs = settings.TEMPLATES[0]['DIRS']
        for template_dir in template_dirs:
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        path = os.path.join(root, file)
                        rel_path = os.path.relpath(path, template_dir).replace('\\', '/')
                        try:
                            get_template(rel_path)
                        except TemplateSyntaxError as e:
                            self.stdout.write(self.style.ERROR(f'[SYNTAX ERROR] {rel_path}: {e}'))
                            template_errors += 1
                        except TemplateDoesNotExist:
                            pass
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'[ERROR] {rel_path}: {e}'))
                            template_errors += 1
        if template_errors == 0:
            self.stdout.write(self.style.SUCCESS('All templates compiled successfully.'))
        else:
            self.stdout.write(self.style.ERROR(f'Found {template_errors} template errors.'))
        self.stdout.write('\n2. Listing All Valid URLs...')
        resolver = get_resolver()
        try:
            url_count = self.count_patterns(resolver.url_patterns)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {url_count} URL patterns.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'URL Configuration Error: {e}'))
    def count_patterns(self, patterns):
        count = 0
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                count += 1
            elif isinstance(pattern, URLResolver):
                count += self.count_patterns(pattern.url_patterns)
        return count

--- apps\crm\admin.py ---
from django.contrib import admin
from .models import LeadSource, Stage, Lead, Activity
@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'utm_source')
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_won', 'color')
    list_editable = ('order', 'color')
class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    readonly_fields = ('created_at',)
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'source', 'stage', 'assigned_to', 'created_at')
    list_filter = ('stage', 'source', 'assigned_to')
    search_fields = ('full_name', 'phone')
    inlines = [ActivityInline]

--- apps\crm\apps.py ---
from django.apps import AppConfig
class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crm'
    verbose_name = "Sotuv Bo'limi (CRM)"

--- apps\crm\forms.py ---
from django import forms
from .models import Lead, Stage, LeadSource
INPUT_CLASSES = "w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'source', 'interested_course', 'extra_data']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ism Familiya'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '998901234567'}),
            'source': forms.Select(attrs={'class': INPUT_CLASSES}),
            'interested_course': forms.Select(attrs={'class': INPUT_CLASSES}),
            'extra_data': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': "Qo'shimcha izohlar..."}),
        }
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if self.organization:
            self.fields['source'].queryset = LeadSource.objects.filter(
                organization=self.organization, is_deleted=False
            )
            from apps.education.models import Course
            self.fields['interested_course'].queryset = Course.objects.filter(
                organization=self.organization, is_deleted=False
            )
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'order', 'color', 'is_won']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': "Masalan: Yangi, Qo'ng'iroq qilindi"
            }),
            'order': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'min': 1
            }),
            'color': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'type': 'color',
                'style': 'height: 42px;'
            }),
            'is_won': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary rounded'
            }),
        }
class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields = ['name', 'utm_source']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Instagram, Telegram, Ko\'cha'
            }),
            'utm_source': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'ig_ads_summer'
            }),
        }
class LeadConvertForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ism'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Familiya'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES})
    )
    password = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Parol (bo\'sh qoldirsangiz avtomatik yaratiladi)'})
    )
    parent_first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ota-ona ismi'})
    )
    parent_last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ota-ona familiyasi'})
    )
    parent_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': "Ota-ona telefon raqami"})
    )
    relation_type = forms.ChoiceField(
        choices=[
            ('father', 'Otasi'),
            ('mother', 'Onasi'),
            ('guardian', 'Vasiysi'),
            ('relative', 'Qarindoshi'),
        ],
        widget=forms.Select(attrs={'class': INPUT_CLASSES})
    )

--- apps\crm\models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.education.models import Course
class LeadSource(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Manba nomi")
    utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Kodo")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'lead_sources'
        verbose_name = "Lid Manbasi"
        verbose_name_plural = "Lid Manbalari"
class Stage(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Bosqich nomi")
    order = models.PositiveIntegerField(default=1, verbose_name="Ketma-ketlik")
    color = models.CharField(max_length=20, default="
    is_won = models.BooleanField(default=False,
                                 verbose_name="Yutuq bosqichimi?")
    class Meta:
        db_table = 'crm_stages'
        ordering = ['order']
        verbose_name = "Voronka Bosqichi"
        verbose_name_plural = "Voronka Bosqichlari"
    def __str__(self):
        return self.name
class Lead(TenantAwareModel):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ismi")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, verbose_name="Manba")
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name='leads', verbose_name="Bosqich")
    interested_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Qiziqqan kursi")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    limit_choices_to={'role__in': ['admin', 'owner', 'manager']},
                                    verbose_name="Mas'ul xodim")
    extra_data = models.JSONField(default=dict, blank=True, verbose_name="Qo'shimcha Info")
    def __str__(self):
        return f"{self.full_name} ({self.phone})"
    class Meta:
        db_table = 'leads'
        verbose_name = "Lid"
        verbose_name_plural = "Lidlar"
class Activity(TenantAwareModel):
    TYPE_CHOICES = (
        ('call', 'Qo\'ng\'iroq'),
        ('sms', 'SMS'),
        ('meeting', 'Uchrashuv'),
        ('note', 'Izoh'),
        ('status_change', 'Status o\'zgardi'),
    )
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Bajardi")
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    comment = models.TextField(verbose_name="Izoh/Natija")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'lead_activities'
        ordering = ['-created_at']
        verbose_name = "Harakat"
        verbose_name_plural = "Harakatlar"

--- apps\crm\services.py ---
from django.db import transaction
from apps.users.models import User
from apps.crm.models import Lead, Activity
def convert_lead_to_student(lead_id, user_id=None):
    lead = Lead.objects.get(id=lead_id)
    if User.objects.filter(phone=lead.phone).exists():
        return None, "Bu raqamli foydalanuvchi allaqachon mavjud."
    with transaction.atomic():
        new_student = User.objects.create_user(
            phone=lead.phone,
            password='student123',
            first_name=lead.full_name.split()[0],
            last_name=lead.full_name.split()[-1] if len(lead.full_name.split()) > 1 else "",
            role='student',
            organization=lead.organization
        )
        Activity.objects.create(
            organization=lead.organization,
            lead=lead,
            user_id=user_id,
            activity_type='status_change',
            comment="Lid muvaffaqiyatli O'quvchiga aylantirildi!"
        )
        return new_student, "Muvaffaqiyatli o'tkazildi"
def move_lead_to_stage(lead_id, new_stage_id, user_id):
    lead = Lead.objects.get(id=lead_id)
    old_stage = lead.stage.name
    lead.stage_id = new_stage_id
    lead.save()
    Activity.objects.create(
        organization=lead.organization,
        lead=lead,
        user_id=user_id,
        activity_type='status_change',
        comment=f"Status o'zgardi: {old_stage} -> {lead.stage.name}"
    )
    return lead

--- apps\crm\urls.py ---
from django.urls import path
from . import views
urlpatterns = [
    path('pipeline/', views.pipeline_view, name='pipeline'),
    path('leads/add/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),
    path('leads/<int:pk>/convert/', views.lead_convert, name='lead_convert'),
    path('leads/<int:pk>/activity/', views.add_lead_activity, name='add_lead_activity'),
    path('api/leads/<int:lead_id>/move/', views.update_lead_stage, name='update_lead_stage'),
    path('stages/', views.stage_list, name='stage_list'),
    path('stages/add/', views.stage_create, name='stage_create'),
    path('stages/<int:pk>/edit/', views.stage_edit, name='stage_edit'),
    path('stages/<int:pk>/delete/', views.stage_delete, name='stage_delete'),
    path('sources/', views.source_list, name='source_list'),
    path('sources/add/', views.source_create, name='source_create'),
    path('sources/<int:pk>/edit/', views.source_edit, name='source_edit'),
    path('sources/<int:pk>/delete/', views.source_delete, name='source_delete'),
]

--- apps\crm\views.py ---
import json
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Prefetch, Count
from .models import Lead, Stage, LeadSource, Activity
from .forms import LeadForm, StageForm, LeadSourceForm, LeadConvertForm
from .services import move_lead_to_stage
from apps.users.models import User, ParentStudent
from apps.core.audit import log_user_action
@login_required
def pipeline_view(request):
    org = request.organization
    stages = Stage.objects.filter(organization=org, is_deleted=False) \
        .order_by('order') \
        .prefetch_related(
            Prefetch('leads', queryset=Lead.objects.filter(
                organization=org, is_deleted=False
            ).select_related('source', 'interested_course').order_by('-created_at'))
        )
    total_leads = Lead.objects.filter(organization=org, is_deleted=False).count()
    return render(request, 'crm/pipeline.html', {
        'stages': stages,
        'total_leads': total_leads,
    })
@login_required
def lead_create(request):
    org = request.organization
    if request.method == 'POST':
        form = LeadForm(request.POST, organization=org)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.organization = org
            first_stage = Stage.objects.filter(
                organization=org, is_deleted=False
            ).order_by('order').first()
            if not first_stage:
                messages.error(request, "Avval bosqichlarni (Stages) yarating!")
                return redirect('stage_list')
            lead.stage = first_stage
            lead.assigned_to = request.user
            lead.save()
            log_user_action(request.user, 'CREATE', 'Lead', lead.id, str(lead), request=request)
            messages.success(request, "Lid muvaffaqiyatli qo'shildi!")
            return redirect('pipeline')
    else:
        form = LeadForm(organization=org)
    return render(request, 'crm/lead_form.html', {'form': form, 'title': "Yangi Lid"})
@login_required
def lead_detail(request, pk):
    org = request.organization
    lead = get_object_or_404(Lead, pk=pk, organization=org, is_deleted=False)
    activities = Activity.objects.filter(lead=lead).select_related('user').order_by('-created_at')
    stages = Stage.objects.filter(organization=org, is_deleted=False).order_by('order')
    return render(request, 'crm/lead_detail.html', {
        'lead': lead,
        'activities': activities,
        'stages': stages,
    })
@login_required
def lead_edit(request, pk):
    org = request.organization
    lead = get_object_or_404(Lead, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead, organization=org)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'Lead', lead.id, str(lead), request=request)
            messages.success(request, "Lid yangilandi!")
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead, organization=org)
    return render(request, 'crm/lead_form.html', {'form': form, 'title': "Lidni tahrirlash", 'lead': lead})
@login_required
def lead_delete(request, pk):
    org = request.organization
    lead = get_object_or_404(Lead, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        lead.delete()
        log_user_action(request.user, 'DELETE', 'Lead', lead.id, str(lead), request=request)
        messages.warning(request, "Lid o'chirildi!")
        return redirect('pipeline')
    return render(request, 'crm/lead_confirm_delete.html', {'lead': lead})
@login_required
def lead_convert(request, pk):
    org = request.organization
    lead = get_object_or_404(Lead, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        form = LeadConvertForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            parent, created = User.objects.get_or_create(
                phone=data['parent_phone'],
                defaults={
                    'first_name': data['parent_first_name'],
                    'last_name': data.get('parent_last_name', ''),
                    'role': 'parent',
                    'organization': org,
                }
            )
            if created:
                parent.set_password(secrets.token_urlsafe(8))
                parent.save()
            password = data.get('password') or secrets.token_urlsafe(8)
            student = User.objects.create(
                phone=data['phone'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role='student',
                organization=org,
            )
            student.set_password(password)
            student.save()
            from .models import ParentStudent
            ParentStudent.objects.create(
                organization=org,
                parent=parent,
                student=student,
                relation_type=data['relation_type'],
                is_main_contact=True,
            )
            from .models import Stage
            won_stage = Stage.objects.filter(organization=org, is_won=True).first()
            if won_stage:
                lead.stage = won_stage
                lead.save()
            Activity.objects.create(
                organization=org,
                lead=lead,
                user=request.user,
                activity_type='status_change',
                comment=f"O'quvchiga aylandi: {student.first_name} {student.last_name}"
            )
            log_user_action(request.user, 'CREATE', 'User', student.id, str(student),
                           changes={'converted_from_lead': lead.id}, request=request)
            messages.success(request, f"O'quvchi muvaffaqiyatli yaratildi! Parol: {password}")
            return redirect('user_list')
    else:
        name_parts = lead.full_name.split(' ', 1)
        initial = {
            'first_name': name_parts[0] if name_parts else '',
            'last_name': name_parts[1] if len(name_parts) > 1 else '',
            'phone': lead.phone,
        }
        form = LeadConvertForm(initial=initial)
    return render(request, 'crm/lead_convert.html', {'form': form, 'lead': lead})
@require_POST
@login_required
def update_lead_stage(request, lead_id):
    try:
        data = json.loads(request.body)
        new_stage_id = data.get('stage_id')
        move_lead_to_stage(lead_id, new_stage_id, request.user)
        log_user_action(request.user, 'UPDATE', 'Lead', lead_id,
                       changes={'stage_id': new_stage_id}, request=request)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
@login_required
def add_lead_activity(request, pk):
    org = request.organization
    lead = get_object_or_404(Lead, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type', 'note')
        comment = request.POST.get('comment', '')
        Activity.objects.create(
            organization=org,
            lead=lead,
            user=request.user,
            activity_type=activity_type,
            comment=comment,
        )
        messages.success(request, "Faoliyat qo'shildi!")
    return redirect('lead_detail', pk=pk)
@login_required
def stage_list(request):
    org = request.organization
    stages = Stage.objects.filter(organization=org, is_deleted=False).annotate(
        lead_count=Count('leads', filter=models.Q(leads__is_deleted=False))
    ).order_by('order')
    return render(request, 'crm/stage_list.html', {'stages': stages})
@login_required
def stage_create(request):
    org = request.organization
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.organization = org
            stage.save()
            log_user_action(request.user, 'CREATE', 'Stage', stage.id, str(stage), request=request)
            messages.success(request, "Bosqich yaratildi!")
            return redirect('stage_list')
    else:
        max_order = Stage.objects.filter(organization=org).count() + 1
        form = StageForm(initial={'order': max_order, 'color': '
    return render(request, 'crm/stage_form.html', {'form': form, 'title': "Yangi Bosqich"})
@login_required
def stage_edit(request, pk):
    org = request.user.organization
    stage = get_object_or_404(Stage, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'Stage', stage.id, str(stage), request=request)
            messages.success(request, "Bosqich yangilandi!")
            return redirect('stage_list')
    else:
        form = StageForm(instance=stage)
    return render(request, 'crm/stage_form.html', {'form': form, 'title': "Bosqichni tahrirlash"})
@login_required
def stage_delete(request, pk):
    org = request.user.organization
    stage = get_object_or_404(Stage, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        if stage.leads.filter(is_deleted=False).exists():
            messages.error(request, "Bu bosqichda lidlar bor! Avval ularni boshqa bosqichga o'tkazing.")
            return redirect('stage_list')
        stage.delete()
        log_user_action(request.user, 'DELETE', 'Stage', stage.id, str(stage), request=request)
        messages.warning(request, "Bosqich o'chirildi!")
        return redirect('stage_list')
    return render(request, 'crm/stage_confirm_delete.html', {'stage': stage})
@login_required
def source_list(request):
    org = request.user.organization
    sources = LeadSource.objects.filter(organization=org, is_deleted=False).annotate(
        lead_count=Count('lead', filter=~models.Q(lead__is_deleted=True))
    )
    return render(request, 'crm/source_list.html', {'sources': sources})
@login_required
def source_create(request):
    org = request.user.organization
    if request.method == 'POST':
        form = LeadSourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.organization = org
            source.save()
            log_user_action(request.user, 'CREATE', 'LeadSource', source.id, str(source), request=request)
            messages.success(request, "Manba yaratildi!")
            return redirect('source_list')
    else:
        form = LeadSourceForm()
    return render(request, 'crm/source_form.html', {'form': form, 'title': "Yangi Manba"})
@login_required
def source_edit(request, pk):
    org = request.user.organization
    source = get_object_or_404(LeadSource, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        form = LeadSourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'LeadSource', source.id, str(source), request=request)
            messages.success(request, "Manba yangilandi!")
            return redirect('source_list')
    else:
        form = LeadSourceForm(instance=source)
    return render(request, 'crm/source_form.html', {'form': form, 'title': "Manbani tahrirlash"})
@login_required
def source_delete(request, pk):
    org = request.user.organization
    source = get_object_or_404(LeadSource, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        source.delete()
        log_user_action(request.user, 'DELETE', 'LeadSource', source.id, str(source), request=request)
        messages.warning(request, "Manba o'chirildi!")
        return redirect('source_list')
    return render(request, 'crm/source_confirm_delete.html', {'source': source})
from django.db import models

--- apps\education\admin.py ---
from django.contrib import admin
from .models import Room, Course, Group, GroupStudent
from .forms import GroupForm
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'has_projector')
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months', 'is_active')
class StudentInline(admin.TabularInline):
    model = GroupStudent
    extra = 1
    autocomplete_fields = ['student']
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ('name', 'course', 'teacher', 'room', 'start_time', 'status')
    list_filter = ('status', 'course', 'teacher')
    inlines = [StudentInline]
    search_fields = ('name',)
@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'status', 'joined_at')
    list_filter = ('status', 'group')
    search_fields = ('student__phone', 'student__first_name')

--- apps\education\apps.py ---
from django.apps import AppConfig
class EducationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.education'
    verbose_name = "Ta'lim Bo'limi"

--- apps\education\forms.py ---
from django import forms
from apps.users.models import User
from .models import Course, Room, Group
from .services.scheduling import check_schedule_conflict
INPUT_CLASSES = "w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'price', 'duration_months', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'M: General English'}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'duration_months': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-primary'}),
        }
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'has_projector']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'M: 1-xona'}),
            'capacity': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'has_projector': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-primary'}),
        }
class GroupForm(forms.ModelForm):
    DAYS_CHOICES = (
        (1, 'Dushanba'),
        (2, 'Seshanba'),
        (3, 'Chorshanba'),
        (4, 'Payshanba'),
        (5, 'Juma'),
        (6, 'Shanba'),
        (7, 'Yakshanba'),
    )
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if self.organization:
            self.fields['course'].queryset = Course.objects.filter(organization=self.organization, is_deleted=False)
            self.fields['teacher'].queryset = User.objects.filter(organization=self.organization, role='teacher', is_deleted=False)
            self.fields['room'].queryset = Room.objects.filter(organization=self.organization, is_deleted=False)
        self.fields['schedule_days'].choices = self.DAYS_CHOICES
    class Meta:
        model = Group
        fields = ['name', 'course', 'teacher', 'room', 'start_date', 'schedule_days', 'start_time', 'end_time',
                  'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'M: IELTS-A'}),
            'course': forms.Select(attrs={'class': INPUT_CLASSES}),
            'teacher': forms.Select(attrs={'class': INPUT_CLASSES}),
            'room': forms.Select(attrs={'class': INPUT_CLASSES}),
            'start_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': INPUT_CLASSES, 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': INPUT_CLASSES, 'type': 'time'}),
            'status': forms.Select(attrs={'class': INPUT_CLASSES}),
            'schedule_days': forms.SelectMultiple(attrs={'class': INPUT_CLASSES, 'style': 'height: 120px;'}),
        }
    def clean_schedule_days(self):
        days = self.cleaned_data.get('schedule_days')
        if days:
            try:
                return [int(d) for d in days]
            except (ValueError, TypeError):
                return days
        return days
    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        teacher = cleaned_data.get('teacher')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        days = cleaned_data.get('schedule_days') or []
        if room and teacher and days and start_time and end_time:
            org = self.instance.organization if self.instance.pk else None
            msg = check_schedule_conflict(
                organization=org,
                room=room,
                teacher=teacher,
                days=days,
                start_time=start_time,
                end_time=end_time,
                exclude_group_id=self.instance.pk
            )
            if msg:
                raise forms.ValidationError(msg)
        return cleaned_data
class MaterialForm(forms.ModelForm):
    class Meta:
        from apps.education.materials import Material
        model = Material
        fields = [
            'category', 'title', 'description', 'material_type',
            'file', 'external_url', 'thumbnail',
            'access_type', 'groups',
            'is_published', 'is_featured'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Material sarlavhasi'
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 3,
                'placeholder': 'Qisqa tavsif...'
            }),
            'material_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'file': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
                'accept': '.pdf,.doc,.docx,.mp4,.mp3,.zip,.pptx'
            }),
            'external_url': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'https://youtube.com/...'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
                'accept': 'image/*'
            }),
            'access_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'groups': forms.SelectMultiple(attrs={
                'class': INPUT_CLASSES,
                'size': 5
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-300 text-primary focus:ring-primary'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-300 text-amber-500 focus:ring-amber-500'
            }),
        }
    def __init__(self, *args, **kwargs):
        from apps.education.materials import MaterialCategory
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['category'].queryset = MaterialCategory.objects.filter(
                organization=organization, is_deleted=False
            )
            self.fields['groups'].queryset = Group.objects.filter(
                organization=organization, is_deleted=False
            )
        self.fields['category'].required = False
        self.fields['description'].required = False
        self.fields['file'].required = False
        self.fields['external_url'].required = False
        self.fields['thumbnail'].required = False
        self.fields['groups'].required = False

--- apps\education\lms.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.education.models import Course, Group
class ResourceCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    icon = models.CharField(max_length=50, default='ph-folder', verbose_name="Ikonka")
    class Meta:
        db_table = 'lms_categories'
        verbose_name = "Resurs kategoriyasi"
        verbose_name_plural = "Resurs kategoriyalari"
    def __str__(self):
        return self.name
class Resource(TenantAwareModel):
    TYPE_CHOICES = (
        ('pdf', 'PDF Hujjat'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('link', 'Havola'),
        ('document', 'Boshqa hujjat'),
    )
    ACCESS_CHOICES = (
        ('public', 'Hammaga ochiq'),
        ('course', 'Faqat kursga'),
        ('group', 'Faqat guruhga'),
        ('paid', 'Pullik'),
    )
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, related_name='resources')
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pdf', verbose_name="Turi")
    file = models.FileField(upload_to='resources/%Y/%m/', null=True, blank=True, verbose_name="Fayl")
    external_url = models.URLField(blank=True, verbose_name="Tashqi havola")
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', null=True, blank=True, verbose_name="Rasm")
    access_type = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='course', verbose_name="Kirish turi")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='resources', verbose_name="Kurs")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='resources', verbose_name="Guruh")
    file_size = models.PositiveIntegerField(default=0, verbose_name="Fayl hajmi (KB)")
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name="Davomiyligi (daqiqa)")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Yuklab olishlar")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_resources')
    class Meta:
        db_table = 'lms_resources'
        ordering = ['-created_at']
        verbose_name = "Resurs"
        verbose_name_plural = "Resurslar"
    def __str__(self):
        return self.title
    def can_access(self, user):
        if self.access_type == 'public':
            return True
        if user.role in ['super_admin', 'owner', 'admin']:
            return True
        if self.access_type == 'course' and self.course:
            from apps.education.models import GroupEnrollment
            return GroupEnrollment.objects.filter(
                student=user,
                group__course=self.course,
                status='active'
            ).exists()
        if self.access_type == 'group' and self.group:
            from apps.education.models import GroupEnrollment
            return GroupEnrollment.objects.filter(
                student=user,
                group=self.group,
                status='active'
            ).exists()
        if self.access_type == 'paid':
            return ResourceAccess.objects.filter(
                student=user,
                resource=self,
                is_active=True
            ).exists()
        return False
class ResourceAccess(TenantAwareModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_accesses')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='accesses')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Muddati tugaydi")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    class Meta:
        db_table = 'lms_resource_access'
        verbose_name = "Resurs kirish huquqi"
        verbose_name_plural = "Resurs kirish huquqlari"
        unique_together = ('student', 'resource')
class ResourceView(TenantAwareModel):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_views')
    progress_percent = models.PositiveIntegerField(default=0, verbose_name="Progress (%)")
    last_position = models.PositiveIntegerField(default=0, verbose_name="Oxirgi pozitsiya (soniya)")
    completed = models.BooleanField(default=False, verbose_name="Tugallandi")
    class Meta:
        db_table = 'lms_resource_views'
        ordering = ['-updated_at']
        verbose_name = "Resurs ko'rish"
        verbose_name_plural = "Resurs ko'rishlar"
    def __str__(self):
        return f"{self.user.full_name} - {self.resource.title}"

--- apps\education\lms_models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class MaterialCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    icon = models.CharField(max_length=50, default='ph-file', verbose_name="Ikonka")
    color = models.CharField(max_length=20, default='blue', verbose_name="Rang")
    class Meta:
        db_table = 'material_categories'
        verbose_name = "Material kategoriyasi"
        verbose_name_plural = "Material kategoriyalari"
    def __str__(self):
        return self.name
class CourseMaterial(TenantAwareModel):
    TYPE_CHOICES = (
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('document', 'Hujjat'),
        ('presentation', 'Prezentatsiya'),
        ('audio', 'Audio'),
        ('link', 'Havola'),
        ('other', 'Boshqa'),
    )
    course = models.ForeignKey(
        'education.Course',
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name="Kurs"
    )
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='document', verbose_name="Turi")
    file = models.FileField(upload_to='materials/%Y/%m/', null=True, blank=True, verbose_name="Fayl")
    external_url = models.URLField(blank=True, verbose_name="Tashqi havola")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_public = models.BooleanField(default=False, verbose_name="Hammaga ochiqmi?")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya qilingan")
    file_size = models.PositiveIntegerField(default=0, verbose_name="Fayl hajmi (bytes)")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name="Davomiyligi (soniya)")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rildi")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Yuklab olindi")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_materials')
    class Meta:
        db_table = 'course_materials'
        ordering = ['order', 'created_at']
        verbose_name = "Kurs materiali"
        verbose_name_plural = "Kurs materiallari"
    def __str__(self):
        return f"{self.course.name} - {self.title}"
    @property
    def file_size_display(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
    @property
    def duration_display(self):
        if not self.duration_seconds:
            return None
        mins, secs = divmod(self.duration_seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"
class MaterialProgress(TenantAwareModel):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='material_progress',
        limit_choices_to={'role': 'student'}
    )
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False, verbose_name="Tugallandimi?")
    progress_percent = models.PositiveIntegerField(default=0, verbose_name="Progress (%)")
    last_position = models.PositiveIntegerField(default=0, verbose_name="Oxirgi pozitsiya (sekund)")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'material_progress'
        unique_together = ('student', 'material')
        verbose_name = "Material progressi"
        verbose_name_plural = "Material progresslari"
    def __str__(self):
        return f"{self.student.first_name} - {self.material.title}: {self.progress_percent}%"

--- apps\education\lms_views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count, Q
from apps.education.models import Course
from apps.education.lms_models import CourseMaterial, MaterialProgress
from apps.core.audit import log_user_action
@login_required
def material_list(request):
    org = request.user.organization
    if request.user.role in ['super_admin', 'owner', 'admin', 'teacher']:
        courses = Course.objects.filter(organization=org, is_deleted=False, is_active=True)
    else:
        from apps.education.models import GroupStudent
        enrolled_courses = GroupStudent.objects.filter(
            student=request.user,
            status='active'
        ).values_list('group__course_id', flat=True).distinct()
        courses = Course.objects.filter(id__in=enrolled_courses, is_deleted=False)
    courses = courses.annotate(material_count=Count('materials'))
    course_id = request.GET.get('course')
    materials = CourseMaterial.objects.filter(organization=org, is_deleted=False)
    if course_id:
        materials = materials.filter(course_id=course_id)
    elif courses.exists():
        materials = materials.filter(course__in=courses)
    materials = materials.select_related('course', 'uploaded_by').order_by('order', '-created_at')
    material_type = request.GET.get('type')
    if material_type:
        materials = materials.filter(material_type=material_type)
    total_materials = materials.count()
    context = {
        'courses': courses,
        'materials': materials,
        'total_materials': total_materials,
        'current_course': course_id,
        'current_type': material_type,
        'type_choices': CourseMaterial.TYPE_CHOICES,
    }
    return render(request, 'education/material_list.html', context)
@login_required
def material_detail(request, pk):
    org = request.user.organization
    material = get_object_or_404(CourseMaterial, pk=pk, organization=org)
    material.view_count += 1
    material.save(update_fields=['view_count'])
    if request.user.role == 'student':
        progress, created = MaterialProgress.objects.get_or_create(
            student=request.user,
            material=material,
            defaults={'organization': org}
        )
        if created:
            log_user_action(request.user, 'CREATE', 'MaterialProgress',
                           progress.id, f"Started: {material.title}", request=request)
    related_materials = CourseMaterial.objects.filter(
        course=material.course,
        is_deleted=False
    ).exclude(id=material.id).order_by('order')[:5]
    context = {
        'material': material,
        'related_materials': related_materials,
    }
    return render(request, 'education/material_detail.html', context)
@login_required
def material_upload(request, course_id):
    org = request.user.organization
    course = get_object_or_404(Course, pk=course_id, organization=org)
    if request.user.role not in ['super_admin', 'owner', 'admin', 'teacher']:
        messages.error(request, "Sizda material yuklash huquqi yo'q!")
        return redirect('education:material_list')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        material_type = request.POST.get('material_type', 'document')
        file = request.FILES.get('file')
        external_url = request.POST.get('external_url', '')
        is_public = request.POST.get('is_public') == 'on'
        material = CourseMaterial.objects.create(
            organization=org,
            course=course,
            title=title,
            description=description,
            material_type=material_type,
            file=file,
            external_url=external_url,
            is_public=is_public,
            uploaded_by=request.user,
            file_size=file.size if file else 0,
        )
        log_user_action(request.user, 'CREATE', 'CourseMaterial',
                       material.id, title, request=request)
        messages.success(request, f"'{title}' materiali muvaffaqiyatli yuklandi!")
        return redirect('education:material_list')
    context = {
        'course': course,
        'type_choices': CourseMaterial.TYPE_CHOICES,
    }
    return render(request, 'education/material_upload.html', context)
@login_required
def mark_material_complete(request, pk):
    if request.method == 'POST' and request.user.role == 'student':
        org = request.user.organization
        material = get_object_or_404(CourseMaterial, pk=pk, organization=org)
        progress, created = MaterialProgress.objects.get_or_create(
            student=request.user,
            material=material,
            defaults={'organization': org}
        )
        progress.is_completed = True
        progress.progress_percent = 100
        progress.completed_at = timezone.now()
        progress.save()
        return JsonResponse({'status': 'success', 'message': "Material tugallandi!"})
    return JsonResponse({'status': 'error', 'message': "Noto'g'ri so'rov"}, status=400)

--- apps\education\materials.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.education.models import Group
class MaterialCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    icon = models.CharField(max_length=50, default='📁', verbose_name="Ikonka")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    class Meta:
        db_table = 'material_categories'
        ordering = ['order', 'name']
        verbose_name = "Material kategoriyasi"
        verbose_name_plural = "Material kategoriyalari"
    def __str__(self):
        return f"{self.icon} {self.name}"
class Material(TenantAwareModel):
    TYPE_CHOICES = (
        ('video', '🎬 Video'),
        ('pdf', '📄 PDF'),
        ('audio', '🎧 Audio'),
        ('doc', '📝 Hujjat'),
        ('link', '🔗 Havola'),
        ('other', '📦 Boshqa'),
    )
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='materials', verbose_name="Kategoriya")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pdf',
                                     verbose_name="Turi")
    file = models.FileField(upload_to='materials/%Y/%m/', null=True, blank=True,
                           verbose_name="Fayl")
    external_url = models.URLField(null=True, blank=True, verbose_name="Tashqi havola")
    thumbnail = models.ImageField(upload_to='materials/thumbnails/', null=True, blank=True,
                                  verbose_name="Muqova rasmi")
    ACCESS_CHOICES = (
        ('all', 'Hamma uchun'),
        ('group', 'Faqat guruh a\'zolari'),
        ('private', 'Tanlangan o\'quvchilar'),
    )
    access_type = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='all',
                                   verbose_name="Kirish huquqi")
    groups = models.ManyToManyField(Group, blank=True, related_name='materials',
                                    verbose_name="Guruhlar")
    allowed_students = models.ManyToManyField(User, blank=True, related_name='private_materials',
                                              limit_choices_to={'role': 'student'},
                                              verbose_name="Ruxsat berilgan o'quvchilar")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='uploaded_materials', verbose_name="Yukladi")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Yuklab olishlar")
    is_published = models.BooleanField(default=True, verbose_name="Chop etilgan")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    class Meta:
        db_table = 'materials'
        ordering = ['-created_at']
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
    def __str__(self):
        return f"{self.get_material_type_display()} {self.title}"
    @property
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return round(self.file.size / (1024 * 1024), 2)
        return 0
    def can_access(self, user):
        if user.role in ['super_admin', 'owner', 'admin', 'teacher']:
            return True
        if self.access_type == 'all':
            return True
        if self.access_type == 'group':
            return self.groups.filter(students=user).exists()
        if self.access_type == 'private':
            return self.allowed_students.filter(pk=user.pk).exists()
        return False
class MaterialView(TenantAwareModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.PositiveIntegerField(default=0, verbose_name="Ko'rish davomiyligi (soniya)")
    class Meta:
        db_table = 'material_views'
        ordering = ['-viewed_at']
        verbose_name = "Material ko'rish"
        verbose_name_plural = "Material ko'rishlar"
    def __str__(self):
        return f"{self.user.first_name} - {self.material.title}"
class Syllabus(TenantAwareModel):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='syllabus',
                                  verbose_name="Guruh")
    title = models.CharField(max_length=255, verbose_name="Reja nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    file = models.FileField(upload_to='syllabi/%Y/', null=True, blank=True,
                           verbose_name="Reja fayli")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='created_syllabi')
    class Meta:
        db_table = 'syllabi'
        verbose_name = "O'quv rejasi"
        verbose_name_plural = "O'quv rejalari"
    def __str__(self):
        return f"{self.group.name} - {self.title}"
class SyllabusItem(TenantAwareModel):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name='items')
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    title = models.CharField(max_length=255, verbose_name="Mavzu")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=1,
                                         verbose_name="Davomiylik (soat)")
    materials = models.ManyToManyField(Material, blank=True, related_name='syllabus_items',
                                       verbose_name="Materiallar")
    is_completed = models.BooleanField(default=False, verbose_name="Yakunlandi")
    completed_at = models.DateField(null=True, blank=True, verbose_name="Yakunlangan sana")
    class Meta:
        db_table = 'syllabus_items'
        ordering = ['syllabus', 'order']
        verbose_name = "O'quv rejasi bandi"
        verbose_name_plural = "O'quv rejasi bandlari"
    def __str__(self):
        return f"{self.order}. {self.title}"

--- apps\education\materials_views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.education.materials import MaterialCategory, Material, MaterialView
from apps.education.models import Group
from apps.core.audit import log_user_action
@login_required
def material_list(request):
    org = request.organization
    user = request.user
    categories = MaterialCategory.objects.filter(organization=org, is_deleted=False)
    category_id = request.GET.get('category', '')
    material_type = request.GET.get('type', '')
    search = request.GET.get('q', '')
    materials = Material.objects.filter(
        organization=org,
        is_deleted=False,
        is_published=True
    ).select_related('category', 'uploaded_by')
    if user.role == 'student':
        student_groups = Group.objects.filter(students__student=user)
        materials = materials.filter(
            Q(access_type='all') |
            Q(access_type='group', groups__in=student_groups) |
            Q(access_type='private', allowed_students=user)
        ).distinct()
    if category_id:
        materials = materials.filter(category_id=category_id)
    if material_type:
        materials = materials.filter(material_type=material_type)
    if search:
        materials = materials.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    featured = materials.filter(is_featured=True)[:4]
    context = {
        'materials': materials[:50],
        'categories': categories,
        'featured': featured,
        'category_id': category_id,
        'material_type': material_type,
        'search': search,
    }
    return render(request, 'education/materials.html', context)
@login_required
def material_view(request, pk):
    org = request.organization
    material = get_object_or_404(Material, pk=pk, organization=org)
    if not material.can_access(request.user):
        messages.error(request, "Bu materialga kirish huquqingiz yo'q!")
        return redirect('material_list')
    MaterialView.objects.create(
        organization=org,
        material=material,
        user=request.user
    )
    material.view_count += 1
    material.save(update_fields=['view_count'])
    context = {
        'material': material,
    }
    return render(request, 'education/material_detail.html', context)
@login_required
def material_download(request, pk):
    from django.http import FileResponse
    org = request.organization
    material = get_object_or_404(Material, pk=pk, organization=org)
    if not material.can_access(request.user):
        messages.error(request, "Bu materialga kirish huquqingiz yo'q!")
        return redirect('material_list')
    if not material.file:
        messages.error(request, "Fayl topilmadi!")
        return redirect('material_list')
    material.download_count += 1
    material.save(update_fields=['download_count'])
    return FileResponse(material.file.open(), as_attachment=True, filename=material.file.name.split('/')[-1])
@login_required
def material_upload(request):
    from .forms import MaterialForm
    org = request.organization
    if request.user.role not in ['super_admin', 'owner', 'admin', 'teacher']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('material_list')
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            material = form.save(commit=False)
            material.organization = org
            material.uploaded_by = request.user
            material.save()
            form.save_m2m()
            log_user_action(request.user, 'CREATE', 'Material', material.id,
                           f"Material yukladi: {material.title}", request=request)
            messages.success(request, f"'{material.title}' muvaffaqiyatli yuklandi!")
            return redirect('material_list')
    else:
        form = MaterialForm(organization=org)
    context = {
        'form': form,
        'title': "Yangi Material Yuklash",
    }
    return render(request, 'education/material_form.html', context)
@login_required
def material_edit(request, pk):
    from .forms import MaterialForm
    org = request.organization
    material = get_object_or_404(Material, pk=pk, organization=org)
    if request.user.role not in ['super_admin', 'owner', 'admin', 'teacher']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('material_list')
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material, organization=org)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'Material', material.id,
                           f"Material tahrirladi: {material.title}", request=request)
            messages.success(request, "Material yangilandi!")
            return redirect('material_list')
    else:
        form = MaterialForm(instance=material, organization=org)
    context = {
        'form': form,
        'material': material,
        'title': "Materialni Tahrirlash",
    }
    return render(request, 'education/material_form.html', context)
@login_required
def material_delete(request, pk):
    org = request.organization
    material = get_object_or_404(Material, pk=pk, organization=org)
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('material_list')
    material.is_deleted = True
    material.save()
    log_user_action(request.user, 'DELETE', 'Material', material.id,
                   f"Material o'chirdi: {material.title}", request=request)
    messages.success(request, "Material o'chirildi!")
    return redirect('material_list')

--- apps\education\models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class Room(TenantAwareModel):
    name = models.CharField(max_length=50, verbose_name="Xona nomi")
    capacity = models.PositiveIntegerField(default=10, verbose_name="Sig'imi")
    has_projector = models.BooleanField(default=False, verbose_name="Proyektor bormi?")
    def __str__(self):
        return f"{self.name} ({self.capacity} kishilik)"
    class Meta:
        db_table = 'rooms'
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
class Course(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kurs nomi")
    description = models.TextField(blank=True, verbose_name="Ta'rif")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi (Oylik)")
    duration_months = models.PositiveIntegerField(default=3, verbose_name="Davomiyligi (oy)")
    is_active = models.BooleanField(default=True, verbose_name="Aktivmi?")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'courses'
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
class Group(TenantAwareModel):
    STATUS_CHOICES = (
        ('pending', 'Yig\'ilmoqda'),
        ('active', 'Dars ketmoqda'),
        ('finished', 'Tugatilgan'),
        ('cancelled', 'Bekor qilingan'),
    )
    name = models.CharField(max_length=100, verbose_name="Guruh nomi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups', verbose_name="Kurs")
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_groups',
        verbose_name="O'qituvchi"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    start_date = models.DateField(null=True, blank=True, verbose_name="Boshlanish sanasi")
    end_date = models.DateField(null=True, blank=True, verbose_name="Tugash sanasi")
    schedule_days = models.JSONField(default=list, verbose_name="Dars kunlari (1=Dush...7=Yak)")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Tugash vaqti")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='groups', verbose_name="Xona")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'groups'
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
class GroupStudent(TenantAwareModel):
    STATUS_CHOICES = (
        ('active', 'O\'qiyapti'),
        ('frozen', 'Muzlatilgan'),
        ('left', 'Chiqib ketgan'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_groups',
        limit_choices_to={'role': 'student'},
        verbose_name="O'quvchi"
    )
    joined_at = models.DateField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status")
    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True, verbose_name="Shartnoma")
    class Meta:
        db_table = 'group_students'
        unique_together = ('group', 'student')
        verbose_name = "Guruh a'zosi"
        verbose_name_plural = "Guruh a'zolari"
from apps.education.materials import MaterialCategory, Material, MaterialView, Syllabus, SyllabusItem

--- apps\education\urls.py ---
from django.urls import path
from . import views
from . import materials_views
urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_create, name='group_create'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/add-student/', views.add_student_to_group, name='add_student_to_group'),
    path('groups/<int:pk>/remove-student/<int:student_id>/', views.remove_student_from_group, name='remove_student_from_group'),
    path('materials/', materials_views.material_list, name='material_list'),
    path('materials/<int:pk>/', materials_views.material_view, name='material_view'),
    path('materials/<int:pk>/download/', materials_views.material_download, name='material_download'),
    path('materials/upload/', materials_views.material_upload, name='material_upload'),
    path('materials/<int:pk>/edit/', materials_views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', materials_views.material_delete, name='material_delete'),
]

--- apps\education\views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Course, Room, Group, GroupStudent
from .forms import CourseForm, RoomForm, GroupForm
from apps.users.models import User
from apps.core.audit import log_user_action
@login_required
def course_list(request):
    org = request.organization
    courses = Course.objects.filter(organization=org, is_deleted=False)
    courses = courses.annotate(
        group_count=Count('groups', filter=Q(groups__is_deleted=False))
    )
    return render(request, 'education/course_list.html', {'courses': courses})
@login_required
def course_create(request):
    org = request.organization
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.organization = org
            course.save()
            log_user_action(request.user, 'CREATE', 'Course', course.id, str(course), request=request)
            messages.success(request, "Kurs yaratildi!")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'education/form.html', {'form': form, 'title': 'Yangi Kurs'})
@login_required
def course_edit(request, pk):
    org = request.organization
    course = get_object_or_404(Course, pk=pk, organization=org)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'Course', course.id, str(course), request=request)
            messages.success(request, "Kurs yangilandi!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'education/form.html', {'form': form, 'title': 'Kursni tahrirlash'})
@login_required
def room_list(request):
    org = request.organization
    rooms = Room.objects.filter(organization=org, is_deleted=False)
    return render(request, 'education/room_list.html', {'rooms': rooms})
@login_required
def room_create(request):
    org = request.organization
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.organization = org
            room.save()
            log_user_action(request.user, 'CREATE', 'Room', room.id, str(room), request=request)
            messages.success(request, "Xona qo'shildi!")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'education/form.html', {'form': form, 'title': 'Yangi Xona'})
@login_required
def group_list(request):
    org = request.organization
    groups = Group.objects.filter(organization=org, is_deleted=False).select_related('course', 'teacher', 'room')
    if request.user.role == 'teacher':
        groups = groups.filter(teacher=request.user)
    groups = groups.annotate(
        student_count=Count('students', filter=Q(students__status='active'))
    )
    return render(request, 'education/group_list.html', {'groups': groups})
@login_required
def group_create(request):
    org = request.organization
    if request.method == 'POST':
        form = GroupForm(request.POST, organization=org)
        if form.is_valid():
            group = form.save(commit=False)
            group.organization = org
            group.save()
            log_user_action(request.user, 'CREATE', 'Group', group.id, str(group), request=request)
            messages.success(request, "Guruh muvaffaqiyatli yaratildi!")
            return redirect('group_list')
        else:
            messages.error(request, "Xatolik! Jadvalda to'qnashuv bo'lishi mumkin.")
    else:
        form = GroupForm(organization=org)
    return render(request, 'education/group_form.html', {'form': form, 'title': 'Yangi Guruh'})
@login_required
def group_detail(request, pk):
    org = request.organization
    group = get_object_or_404(Group, pk=pk, organization=org, is_deleted=False)
    enrollments = GroupStudent.objects.filter(group=group).select_related('student')
    enrolled_ids = enrollments.values_list('student_id', flat=True)
    available_students = User.objects.filter(
        organization=org,
        role='student',
        is_active=True,
        is_deleted=False
    ).exclude(id__in=enrolled_ids)
    context = {
        'group': group,
        'enrollments': enrollments,
        'available_students': available_students,
    }
    return render(request, 'education/group_detail.html', context)
@login_required
def add_student_to_group(request, pk):
    org = request.organization
    group = get_object_or_404(Group, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = get_object_or_404(User, pk=student_id, organization=org, role='student')
            if not GroupStudent.objects.filter(group=group, student=student).exists():
                GroupStudent.objects.create(
                    organization=org,
                    group=group,
                    student=student,
                    status='active'
                )
                log_user_action(request.user, 'CREATE', 'GroupStudent', group.id,
                               f"{student.first_name} -> {group.name}", request=request)
                messages.success(request, f"{student.first_name} guruhga qo'shildi!")
            else:
                messages.warning(request, "Bu o'quvchi allaqachon guruhda!")
    return redirect('group_detail', pk=pk)
@login_required
def remove_student_from_group(request, pk, student_id):
    org = request.organization
    group = get_object_or_404(Group, pk=pk, organization=org, is_deleted=False)
    enrollment = get_object_or_404(GroupStudent, group=group, student_id=student_id)
    if request.method == 'POST':
        enrollment.status = 'left'
        enrollment.save()
        log_user_action(request.user, 'UPDATE', 'GroupStudent', group.id,
                       f"{enrollment.student.first_name} chiqdi", request=request)
        messages.warning(request, "O'quvchi guruhdan chiqarildi.")
    return redirect('group_detail', pk=pk)
@login_required
def group_edit(request, pk):
    org = request.organization
    group = get_object_or_404(Group, pk=pk, organization=org, is_deleted=False)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group, organization=org)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'Group', group.id, str(group), request=request)
            messages.success(request, "Guruh yangilandi!")
            return redirect('group_detail', pk=pk)
    else:
        form = GroupForm(instance=group, organization=org)
    return render(request, 'education/group_form.html', {'form': form, 'title': 'Guruhni tahrirlash', 'group': group})

--- apps\education\services\scheduling.py ---
from apps.education.models import Group
def check_schedule_conflict(organization, room, teacher, days, start_time, end_time, exclude_group_id=None):
    existing_groups = Group.objects.filter(
        organization=organization,
        status__in=['active', 'pending']
    )
    if exclude_group_id:
        existing_groups = existing_groups.exclude(id=exclude_group_id)
    for group in existing_groups:
        common_days = set(group.schedule_days) & set(map(int, days))
        if not common_days:
            continue
        if start_time < group.end_time and end_time > group.start_time:
            if room and group.room == room:
                return f"Xato! {room.name} xonasi '{group.name}' guruhi tomonidan band ({group.start_time} - {group.end_time})."
            if teacher and group.teacher == teacher:
                return f"Xato! O'qituvchi {teacher.first_name} bu vaqtda '{group.name}' guruhida darsda."
    return None

--- apps\finance\admin.py ---
from django.contrib import admin
from django.utils.html import format_html
from .models import Account, TransactionCategory, Transaction
from .services import confirm_transaction
from django.contrib import messages
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'balance', 'organization')
@admin.register(TransactionCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type')
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount_colored', 'transaction_type', 'account', 'student', 'status_colored', 'created_at')
    list_filter = ('status', 'transaction_type', 'account', 'category')
    search_fields = ('student__phone', 'student__first_name', 'description')
    readonly_fields = ('created_by', 'confirmed_by', 'confirmed_at')
    actions = ['approve_transactions']
    def amount_colored(self, obj):
        color = 'green' if obj.transaction_type == 'income' else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{} {:,.0f}</span>', color,
                           "+" if obj.transaction_type == 'income' else "-", obj.amount)
    amount_colored.short_description = "Summa"
    def status_colored(self, obj):
        colors = {'pending': 'orange', 'confirmed': 'green', 'rejected': 'red'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 6px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'), obj.get_status_display())
    status_colored.short_description = "Status"
    def approve_transactions(self, request, queryset):
        count = 0
        for tx in queryset:
            if tx.status == 'pending':
                try:
                    confirm_transaction(tx.id, request.user)
                    count += 1
                except Exception as e:
                    self.message_user(request, f"Xatolik (ID: {tx.id}): {e}", level=messages.ERROR)
        self.message_user(request, f"{count} ta tranzaksiya tasdiqlandi va balanslar yangilandi.")
    approve_transactions.short_description = "Tanlanganlarni tasdiqlash (Balansga o'tkazish)"
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

--- apps\finance\apps.py ---
from django.apps import AppConfig
class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.finance'
    verbose_name = "Moliya va Kassa"

--- apps\finance\cash_register.py ---
from django.db import models
from django.utils import timezone
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.finance.models import Account, Transaction
class CashRegisterSession(TenantAwareModel):
    STATUS_CHOICES = (
        ('open', 'Ochiq'),
        ('pending', 'Yopilmoqda'),
        ('closed', 'Yopilgan'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sessions', verbose_name="Kassa")
    opened_at = models.DateTimeField(default=timezone.now, verbose_name="Ochildi")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Yopildi")
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Boshlang'ich balans")
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Jami kirim")
    total_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Jami chiqim")
    expected_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Kutilgan balans")
    actual_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Haqiqiy balans")
    difference = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Farq")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Holat")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    opened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opened_sessions')
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='closed_sessions')
    class Meta:
        db_table = 'cash_register_sessions'
        ordering = ['-opened_at']
        verbose_name = "Kassa sessiyasi"
        verbose_name_plural = "Kassa sessiyalari"
    def __str__(self):
        return f"{self.account.name} - {self.opened_at.strftime('%d.%m.%Y')}"
    def calculate_totals(self):
        transactions = Transaction.objects.filter(
            account=self.account,
            created_at__gte=self.opened_at,
            status='confirmed'
        )
        if self.closed_at:
            transactions = transactions.filter(created_at__lte=self.closed_at)
        self.total_income = sum(
            t.amount for t in transactions if t.transaction_type in ['income']
        )
        self.total_expense = sum(
            t.amount for t in transactions if t.transaction_type in ['expense', 'salary', 'refund']
        )
        self.expected_balance = self.opening_balance + self.total_income - self.total_expense
        return self.expected_balance
    def close_session(self, actual_balance, closed_by, notes=''):
        self.calculate_totals()
        self.actual_balance = actual_balance
        self.difference = actual_balance - self.expected_balance
        self.closed_at = timezone.now()
        self.closed_by = closed_by
        self.notes = notes
        self.status = 'closed'
        self.save()
        self.account.balance = actual_balance
        self.account.save()
        return self.difference
class DailyReport(TenantAwareModel):
    date = models.DateField(unique=True, verbose_name="Sana")
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    income_count = models.PositiveIntegerField(default=0)
    expense_count = models.PositiveIntegerField(default=0)
    new_students = models.PositiveIntegerField(default=0, verbose_name="Yangi o'quvchilar")
    payments_received = models.PositiveIntegerField(default=0, verbose_name="To'lovlar soni")
    lessons_completed = models.PositiveIntegerField(default=0, verbose_name="O'tilgan darslar")
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Davomat foizi")
    generated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'daily_reports'
        ordering = ['-date']
        verbose_name = "Kunlik hisobot"
        verbose_name_plural = "Kunlik hisobotlar"
    def __str__(self):
        return f"Hisobot - {self.date}"
    @classmethod
    def generate_for_date(cls, organization, date):
        from django.db.models import Sum, Count, Avg
        from datetime import datetime, timedelta
        from apps.operations.models import Lesson, Attendance
        from apps.users.models import User
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        transactions = Transaction.objects.filter(
            organization=organization,
            created_at__range=(start, end),
            status='confirmed'
        )
        income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount'), count=Count('id')
        )
        expense = transactions.filter(transaction_type__in=['expense', 'salary']).aggregate(
            total=Sum('amount'), count=Count('id')
        )
        lessons = Lesson.objects.filter(
            organization=organization,
            date=date,
            status='finished'
        )
        attendances = Attendance.objects.filter(
            lesson__in=lessons
        )
        if attendances.exists():
            present = attendances.filter(status='present').count()
            attendance_rate = (present / attendances.count()) * 100
        else:
            attendance_rate = 0
        new_students = User.objects.filter(
            organization=organization,
            role='student',
            date_joined__date=date
        ).count()
        report, created = cls.objects.update_or_create(
            organization=organization,
            date=date,
            defaults={
                'total_income': income['total'] or 0,
                'income_count': income['count'] or 0,
                'total_expense': expense['total'] or 0,
                'expense_count': expense['count'] or 0,
                'net_profit': (income['total'] or 0) - (expense['total'] or 0),
                'lessons_completed': lessons.count(),
                'attendance_rate': attendance_rate,
                'new_students': new_students,
                'payments_received': income['count'] or 0,
            }
        )
        return report

--- apps\finance\forms.py ---
from django import forms
from .models import Account, Transaction, TransactionCategory
INPUT_CLASSES = "w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:bg-white"
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Masalan: Asosiy kassa'}),
            'account_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'balance': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '0'}),
        }
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Summa', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Izoh...'}),
        }
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['account'].queryset = Account.objects.filter(
                organization=organization, is_deleted=False
            )
            if transaction_type:
                self.fields['category'].queryset = TransactionCategory.objects.filter(
                    organization=organization,
                    transaction_type=transaction_type,
                    is_deleted=False
                )
            if not self.fields['category'].queryset.exists():
                self.fields['category'].help_text = "Diqqat: Hozircha kategoriya yo'q. Avval kategoriya qo'shing."
class StudentPaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'payment_method', 'description', 'receipt_image', 'receipt_file']
        widgets = {
            'account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': "To'lov summasi", 'min': '0'}),
            'payment_method': forms.Select(attrs={'class': INPUT_CLASSES, 'onchange': 'toggleReceiptFields(this)'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 2, 'placeholder': 'Izoh...'}),
            'receipt_image': forms.FileInput(attrs={'class': INPUT_CLASSES, 'accept': 'image/*'}),
            'receipt_file': forms.FileInput(attrs={'class': INPUT_CLASSES, 'accept': '.pdf'}),
        }
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['account'].queryset = Account.objects.filter(organization=organization, is_deleted=False)
            self.fields['category'].queryset = TransactionCategory.objects.filter(organization=organization, transaction_type='income', is_deleted=False)
        self.fields['receipt_image'].required = False
        self.fields['receipt_file'].required = False
        self.fields['description'].required = False

--- apps\finance\inventory.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class AssetCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    icon = models.CharField(max_length=50, default='ph-cube', verbose_name="Ikonka")
    class Meta:
        db_table = 'asset_categories'
        verbose_name = "Aktiv kategoriyasi"
        verbose_name_plural = "Aktiv kategoriyalari"
    def __str__(self):
        return self.name
class Asset(TenantAwareModel):
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('repair', 'Ta\'mirda'),
        ('broken', 'Buzuq'),
        ('disposed', 'Yo\'q qilingan'),
    )
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, related_name='assets')
    name = models.CharField(max_length=200, verbose_name="Nomi")
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name="Inventar raqami")
    room = models.ForeignKey('education.Room', on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='assets', verbose_name="Xona")
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Sotib olish narxi")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="Sotib olingan sana")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Holat")
    condition_notes = models.TextField(blank=True, verbose_name="Holat izohi")
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='responsible_assets', verbose_name="Mas'ul shaxs")
    class Meta:
        db_table = 'assets'
        ordering = ['category', 'name']
        verbose_name = "Aktiv"
        verbose_name_plural = "Aktivlar"
    def __str__(self):
        return f"{self.name} ({self.inventory_number})"
class SupplyCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    class Meta:
        db_table = 'supply_categories'
        verbose_name = "Sarf material kategoriyasi"
        verbose_name_plural = "Sarf material kategoriyalari"
    def __str__(self):
        return self.name
class Supply(TenantAwareModel):
    category = models.ForeignKey(SupplyCategory, on_delete=models.SET_NULL, null=True, related_name='supplies')
    name = models.CharField(max_length=200, verbose_name="Nomi")
    unit = models.CharField(max_length=20, default='dona', verbose_name="O'lchov birligi")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Joriy miqdor")
    min_quantity = models.PositiveIntegerField(default=5, verbose_name="Minimal miqdor")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Birlik narxi")
    class Meta:
        db_table = 'supplies'
        ordering = ['category', 'name']
        verbose_name = "Sarf material"
        verbose_name_plural = "Sarf materiallar"
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity
    @property
    def total_value(self):
        return self.quantity * self.unit_price
class SupplyTransaction(TenantAwareModel):
    TYPE_CHOICES = (
        ('in', 'Kirim'),
        ('out', 'Chiqim'),
    )
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Turi")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supply_transactions')
    notes = models.CharField(max_length=255, blank=True, verbose_name="Izoh")
    class Meta:
        db_table = 'supply_transactions'
        ordering = ['-created_at']
        verbose_name = "Sarf material harakati"
        verbose_name_plural = "Sarf material harakatlari"
    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.transaction_type == 'in':
                self.supply.quantity += self.quantity
            else:
                self.supply.quantity = max(0, self.supply.quantity - self.quantity)
            self.supply.save()
        super().save(*args, **kwargs)

--- apps\finance\inventory_views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, F
from apps.finance.inventory import Supply, SupplyCategory, SupplyTransaction, Asset, AssetCategory
from apps.core.audit import log_user_action
@login_required
def supply_list(request):
    org = request.user.organization
    supplies = Supply.objects.filter(organization=org, is_deleted=False).select_related('category')
    show_low_stock = request.GET.get('low_stock')
    if show_low_stock:
        supplies = supplies.filter(quantity__lte=F('min_quantity'))
    category_id = request.GET.get('category')
    if category_id:
        supplies = supplies.filter(category_id=category_id)
    search = request.GET.get('q')
    if search:
        supplies = supplies.filter(name__icontains=search)
    total_items = supplies.count()
    low_stock_count = supplies.filter(quantity__lte=F('min_quantity')).count()
    total_value = supplies.aggregate(
        total=Sum(F('quantity') * F('unit_price'))
    )['total'] or 0
    categories = SupplyCategory.objects.filter(organization=org, is_deleted=False)
    context = {
        'supplies': supplies,
        'categories': categories,
        'total_items': total_items,
        'low_stock_count': low_stock_count,
        'total_value': total_value,
        'current_category': category_id,
        'current_search': search,
        'show_low_stock': show_low_stock,
    }
    return render(request, 'finance/supply_list.html', context)
@login_required
def supply_add_stock(request, supply_id):
    org = request.user.organization
    supply = get_object_or_404(Supply, pk=supply_id, organization=org)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        if quantity > 0:
            SupplyTransaction.objects.create(
                supply=supply,
                transaction_type='in',
                quantity=quantity,
                performed_by=request.user,
                notes=notes,
                organization=org,
            )
            log_user_action(request.user, 'CREATE', 'SupplyTransaction',
                           None, f"{supply.name}: +{quantity}", request=request)
            messages.success(request, f"{quantity} {supply.unit} qo'shildi!")
    return redirect('finance:supply_list')
@login_required
def supply_remove_stock(request, supply_id):
    org = request.user.organization
    supply = get_object_or_404(Supply, pk=supply_id, organization=org)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        if quantity > 0 and quantity <= supply.quantity:
            SupplyTransaction.objects.create(
                supply=supply,
                transaction_type='out',
                quantity=quantity,
                performed_by=request.user,
                notes=notes,
                organization=org,
            )
            log_user_action(request.user, 'CREATE', 'SupplyTransaction',
                           None, f"{supply.name}: -{quantity}", request=request)
            messages.success(request, f"{quantity} {supply.unit} yechildi!")
        else:
            messages.error(request, "Yetarli miqdor yo'q!")
    return redirect('finance:supply_list')
@login_required
def asset_list(request):
    org = request.user.organization
    assets = Asset.objects.filter(organization=org, is_deleted=False).select_related('category', 'room', 'responsible_person')
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)
    category_id = request.GET.get('category')
    if category_id:
        assets = assets.filter(category_id=category_id)
    total_assets = assets.count()
    active_assets = assets.filter(status='active').count()
    total_value = assets.aggregate(total=Sum('purchase_price'))['total'] or 0
    categories = AssetCategory.objects.filter(organization=org, is_deleted=False)
    context = {
        'assets': assets,
        'categories': categories,
        'total_assets': total_assets,
        'active_assets': active_assets,
        'total_value': total_value,
        'current_status': status,
        'current_category': category_id,
    }
    return render(request, 'finance/asset_list.html', context)

--- apps\finance\models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.finance.payroll import StaffKPI, PayrollRecord, StaffAttendance
from apps.finance.inventory import AssetCategory, Asset, SupplyCategory, Supply, SupplyTransaction
class Account(TenantAwareModel):
    TYPE_CHOICES = (
        ('cash', 'Naqd pul'),
        ('bank', 'Bank hisobi'),
        ('card', 'Korporativ karta'),
        ('wallet', 'Elektron hamyon'),
    )
    name = models.CharField(max_length=100, verbose_name="Kassa nomi")
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cash', verbose_name="Turi")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Joriy Balans")
    def __str__(self):
        return f"{self.name} ({self.balance:,.0f})"
    class Meta:
        db_table = 'finance_accounts'
        verbose_name = "Kassa / Hisob"
        verbose_name_plural = "Kassalar"
class TransactionCategory(TenantAwareModel):
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Turi")
    def __str__(self):
        return f"{self.name} ({self.get_transaction_type_display()})"
    class Meta:
        db_table = 'finance_categories'
        verbose_name = "Tranzaksiya Kategoriyasi"
        verbose_name_plural = "Tranzaksiya Kategoriyalari"
class Transaction(TenantAwareModel):
    TYPE_CHOICES = (
        ('income', 'Kirim (To\'lov)'),
        ('expense', 'Chiqim (Xarajat)'),
        ('transfer', 'O\'tkazma'),
        ('salary', 'Oylik to\'lov'),
        ('refund', 'Pul qaytarish'),
    )
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    )
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions', verbose_name="Kassa")
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments',
                                limit_choices_to={'role': 'student'}, verbose_name="O'quvchi")
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='salaries',
                              limit_choices_to={'role__in': ['teacher', 'staff', 'admin']}, verbose_name="Xodim")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='income', verbose_name="Turi")
    description = models.TextField(blank=True, verbose_name="Izoh")
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Naqd pul'),
        ('card', 'Plastik karta'),
        ('transfer', 'Bank o\'tkazmasi'),
        ('online', 'Online to\'lov'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash',
                                      verbose_name="To'lov usuli")
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/', null=True, blank=True, verbose_name="Chek rasmi")
    receipt_file = models.FileField(upload_to='receipts/%Y/%m/', null=True, blank=True, verbose_name="Chek fayli (PDF)")
    receipt_verified = models.BooleanField(default=False, verbose_name="Chek tasdiqlandi")
    receipt_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name='verified_receipts', verbose_name="Chekni tasdiqladi")
    receipt_verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Tasdiqlash vaqti")
    receipt_notes = models.TextField(blank=True, verbose_name="Chek izohi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_transactions',
                                   verbose_name="Kiritdi")
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='confirmed_transactions', verbose_name="Tasdiqladi")
    confirmed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount:,.0f}"
    class Meta:
        db_table = 'finance_transactions'
        ordering = ['-created_at']
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"

--- apps\finance\payroll.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class StaffKPI(TenantAwareModel):
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='kpi_records',
        limit_choices_to={'role__in': ['teacher', 'staff', 'admin']}
    )
    period_start = models.DateField(verbose_name="Davr boshi")
    period_end = models.DateField(verbose_name="Davr oxiri")
    lessons_completed = models.PositiveIntegerField(default=0, verbose_name="O'tilgan darslar")
    students_count = models.PositiveIntegerField(default=0, verbose_name="O'quvchilar soni")
    students_retained = models.PositiveIntegerField(default=0, verbose_name="Saqlab qolingan o'quvchilar")
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Davomat foizi")
    average_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="O'rtacha baho")
    tasks_completed = models.PositiveIntegerField(default=0, verbose_name="Bajarilgan vazifalar")
    late_count = models.PositiveIntegerField(default=0, verbose_name="Kechikishlar soni")
    absent_count = models.PositiveIntegerField(default=0, verbose_name="Yo'qlamalar soni")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Umumiy ball")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    class Meta:
        db_table = 'staff_kpi'
        ordering = ['-period_end']
        verbose_name = "Xodim KPI"
        verbose_name_plural = "Xodimlar KPI"
        unique_together = ('staff', 'period_start', 'period_end')
    def __str__(self):
        return f"{self.staff.full_name} - {self.period_start} to {self.period_end}"
    def calculate_score(self):
        score = 0
        score += self.lessons_completed * 1
        if self.attendance_rate >= 90:
            score += 10
        elif self.attendance_rate >= 80:
            score += 5
        if self.average_grade >= 80:
            score += 10
        elif self.average_grade >= 70:
            score += 5
        score -= self.late_count * 2
        score -= self.absent_count * 5
        self.total_score = max(0, score)
        return self.total_score
class PayrollRecord(TenantAwareModel):
    STATUS_CHOICES = (
        ('draft', 'Qoralama'),
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('paid', 'To\'langan'),
        ('cancelled', 'Bekor qilingan'),
    )
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payroll_records',
        limit_choices_to={'role__in': ['teacher', 'staff', 'admin']}
    )
    month = models.DateField(verbose_name="Oy (1-sana)")
    base_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Asosiy oylik")
    per_lesson_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Darslik stavka")
    lessons_count = models.PositiveIntegerField(default=0, verbose_name="Darslar soni")
    lesson_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Dars daromadi")
    kpi_bonus = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="KPI bonus")
    other_bonus = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Boshqa bonuslar")
    late_penalty = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Kechikish jarimasi")
    absent_penalty = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Yo'qlama jarimasi")
    other_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Boshqa ushlab qolishlar")
    gross_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Yalpi summa")
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Jami ushlab qolish")
    net_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Qo'lga tegadigan")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Holat")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_payrolls', verbose_name="Tasdiqladi"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'payroll_records'
        ordering = ['-month', 'staff__first_name']
        verbose_name = "Oylik hisob"
        verbose_name_plural = "Oylik hisoblar"
        unique_together = ('staff', 'month')
    def __str__(self):
        return f"{self.staff.full_name} - {self.month.strftime('%B %Y')}"
    def calculate(self):
        self.lesson_earnings = self.per_lesson_rate * self.lessons_count
        self.gross_salary = (
            self.base_salary +
            self.lesson_earnings +
            self.kpi_bonus +
            self.other_bonus
        )
        self.total_deductions = (
            self.late_penalty +
            self.absent_penalty +
            self.other_deductions
        )
        self.net_salary = self.gross_salary - self.total_deductions
        return self.net_salary
class StaffAttendance(TenantAwareModel):
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='staff_attendances',
        limit_choices_to={'role__in': ['teacher', 'staff', 'admin']}
    )
    date = models.DateField(verbose_name="Sana")
    check_in = models.TimeField(null=True, blank=True, verbose_name="Keldi")
    check_out = models.TimeField(null=True, blank=True, verbose_name="Ketdi")
    expected_time = models.TimeField(default='09:00', verbose_name="Kutilgan vaqt")
    late_minutes = models.PositiveIntegerField(default=0, verbose_name="Kechikish (daqiqa)")
    STATUS_CHOICES = (
        ('present', 'Keldi'),
        ('absent', 'Kelmadi'),
        ('late', 'Kechikdi'),
        ('half_day', 'Yarim kun'),
        ('leave', 'Ta\'til'),
        ('sick', 'Kasallik'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present', verbose_name="Holat")
    nfc_check_in = models.BooleanField(default=False, verbose_name="NFC orqali keldimi?")
    nfc_check_out = models.BooleanField(default=False, verbose_name="NFC orqali ketdimi?")
    notes = models.CharField(max_length=255, blank=True, verbose_name="Izoh")
    class Meta:
        db_table = 'staff_attendance'
        ordering = ['-date', 'staff__first_name']
        verbose_name = "Xodim davomati"
        verbose_name_plural = "Xodimlar davomati"
        unique_together = ('staff', 'date')
    def __str__(self):
        return f"{self.staff.full_name} - {self.date}"
    def calculate_late_minutes(self):
        if self.check_in and self.expected_time:
            from datetime import datetime, timedelta
            check_in_dt = datetime.combine(self.date, self.check_in)
            expected_dt = datetime.combine(self.date, self.expected_time)
            if check_in_dt > expected_dt:
                diff = check_in_dt - expected_dt
                self.late_minutes = int(diff.total_seconds() / 60)
                self.status = 'late'
            else:
                self.late_minutes = 0
                self.status = 'present'
        return self.late_minutes

--- apps\finance\payroll_views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import date, timedelta
import calendar
from apps.finance.payroll import StaffKPI, PayrollRecord, StaffAttendance
from apps.finance.models import Account, Transaction, TransactionCategory
from apps.users.models import User
from apps.operations.models import Lesson, Attendance
from apps.core.audit import log_user_action
def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)
@login_required
def payroll_list(request):
    month_str = request.GET.get('month')
    if month_str:
        year, month = map(int, month_str.split('-'))
        selected_month = date(year, month, 1)
    else:
        selected_month = date.today().replace(day=1)
    payrolls = PayrollRecord.objects.filter(
        organization=request.user.organization,
        month=selected_month
    ).select_related('staff', 'approved_by')
    staff_with_payroll = payrolls.values_list('staff_id', flat=True)
    staff_without_payroll = User.objects.filter(
        organization=request.user.organization,
        role__in=['teacher', 'staff', 'admin'],
        is_active=True
    ).exclude(id__in=staff_with_payroll)
    stats = {
        'total_gross': payrolls.aggregate(Sum('gross_salary'))['gross_salary__sum'] or 0,
        'total_net': payrolls.aggregate(Sum('net_salary'))['net_salary__sum'] or 0,
        'approved_count': payrolls.filter(status='approved').count(),
        'pending_count': payrolls.filter(status__in=['draft', 'pending']).count(),
    }
    months = []
    current = date.today().replace(day=1)
    for i in range(12):
        months.append(add_months(current, -i))
    context = {
        'payrolls': payrolls,
        'staff_without_payroll': staff_without_payroll,
        'selected_month': selected_month,
        'months': months,
        'stats': stats,
    }
    return render(request, 'finance/payroll_list.html', context)
@login_required
def calculate_payroll(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id, organization=request.user.organization)
    month_str = request.GET.get('month')
    if month_str:
        year, month = map(int, month_str.split('-'))
        selected_month = date(year, month, 1)
    else:
        selected_month = date.today().replace(day=1)
    payroll, created = PayrollRecord.objects.get_or_create(
        organization=request.user.organization,
        staff=staff,
        month=selected_month,
        defaults={
            'base_salary': staff.profile_data.get('base_salary', 0),
            'per_lesson_rate': staff.profile_data.get('per_lesson_rate', 50000),
        }
    )
    if request.method == 'POST':
        payroll.base_salary = float(request.POST.get('base_salary', 0))
        payroll.per_lesson_rate = float(request.POST.get('per_lesson_rate', 0))
        payroll.kpi_bonus = float(request.POST.get('kpi_bonus', 0))
        payroll.other_bonus = float(request.POST.get('other_bonus', 0))
        payroll.late_penalty = float(request.POST.get('late_penalty', 0))
        payroll.absent_penalty = float(request.POST.get('absent_penalty', 0))
        payroll.other_deductions = float(request.POST.get('other_deductions', 0))
        payroll.notes = request.POST.get('notes', '')
        month_end = add_months(selected_month, 1) - timedelta(days=1)
        lessons_count = Lesson.objects.filter(
            teacher=staff,
            date__gte=selected_month,
            date__lte=month_end,
            status='finished'
        ).count()
        payroll.lessons_count = lessons_count
        payroll.calculate()
        payroll.status = 'pending'
        payroll.save()
        log_user_action(request.user, 'payroll_calculate', payroll)
        messages.success(request, f"{staff.full_name} uchun oylik hisoblandi")
        return redirect('payroll_list')
    month_end = add_months(selected_month, 1) - timedelta(days=1)
    lessons_count = Lesson.objects.filter(
        teacher=staff,
        date__gte=selected_month,
        date__lte=month_end,
        status='finished'
    ).count()
    late_count = StaffAttendance.objects.filter(
        staff=staff,
        date__gte=selected_month,
        date__lte=month_end,
        status='late'
    ).count()
    absent_count = StaffAttendance.objects.filter(
        staff=staff,
        date__gte=selected_month,
        date__lte=month_end,
        status='absent'
    ).count()
    context = {
        'staff': staff,
        'payroll': payroll,
        'selected_month': selected_month,
        'lessons_count': lessons_count,
        'late_count': late_count,
        'absent_count': absent_count,
        'created': created,
    }
    return render(request, 'finance/payroll_calculate.html', context)
@login_required
def approve_payroll(request, pk):
    payroll = get_object_or_404(PayrollRecord, pk=pk, organization=request.user.organization)
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Sizda tasdiqlash huquqi yo'q")
        return redirect('payroll_list')
    payroll.status = 'approved'
    payroll.approved_by = request.user
    payroll.approved_at = timezone.now()
    payroll.save()
    log_user_action(request.user, 'payroll_approve', payroll)
    messages.success(request, f"{payroll.staff.full_name} oyligi tasdiqlandi")
    return redirect('payroll_list')
@login_required
def pay_salary(request, pk):
    payroll = get_object_or_404(PayrollRecord, pk=pk, organization=request.user.organization)
    if payroll.status != 'approved':
        messages.error(request, "Avval oylikni tasdiqlang")
        return redirect('payroll_list')
    if request.method == 'POST':
        account_id = request.POST.get('account')
        account = get_object_or_404(Account, pk=account_id, organization=request.user.organization)
        if account.balance < payroll.net_salary:
            messages.error(request, f"Kassada yetarli mablag' yo'q ({account.balance:,.0f} / {payroll.net_salary:,.0f})")
            return redirect('payroll_list')
        category, _ = TransactionCategory.objects.get_or_create(
            organization=request.user.organization,
            name="Xodimlar oyligi",
            defaults={'transaction_type': 'expense'}
        )
        transaction = Transaction.objects.create(
            organization=request.user.organization,
            account=account,
            category=category,
            staff=payroll.staff,
            amount=payroll.net_salary,
            transaction_type='salary',
            description=f"{payroll.staff.full_name} - {payroll.month.strftime('%B %Y')} oyligi",
            status='confirmed',
            created_by=request.user,
            confirmed_by=request.user,
            confirmed_at=timezone.now()
        )
        account.balance -= payroll.net_salary
        account.save()
        payroll.status = 'paid'
        payroll.paid_at = timezone.now()
        payroll.save()
        log_user_action(request.user, 'salary_paid', payroll)
        messages.success(request, f"{payroll.staff.full_name}ga {payroll.net_salary:,.0f} so'm oylik to'landi")
        return redirect('payroll_list')
    accounts = Account.objects.filter(organization=request.user.organization)
    context = {
        'payroll': payroll,
        'accounts': accounts,
    }
    return render(request, 'finance/payroll_pay.html', context)
@login_required
def staff_attendance_list(request):
    today = date.today()
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = date.fromisoformat(selected_date)
    else:
        selected_date = today
    staff_list = User.objects.filter(
        organization=request.user.organization,
        role__in=['teacher', 'staff', 'admin'],
        is_active=True
    )
    attendances = StaffAttendance.objects.filter(
        organization=request.user.organization,
        date=selected_date
    ).select_related('staff')
    attendance_map = {att.staff_id: att for att in attendances}
    staff_data = []
    for staff in staff_list:
        att = attendance_map.get(staff.id)
        staff_data.append({
            'staff': staff,
            'attendance': att,
            'status': att.status if att else 'unknown',
            'check_in': att.check_in if att else None,
            'check_out': att.check_out if att else None,
        })
    context = {
        'staff_data': staff_data,
        'selected_date': selected_date,
        'today': today,
    }
    return render(request, 'finance/staff_attendance.html', context)
@login_required
def staff_check_in(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id') or request.user.id
        staff = get_object_or_404(User, pk=staff_id, organization=request.user.organization)
        today = date.today()
        now = timezone.now().time()
        att, created = StaffAttendance.objects.get_or_create(
            organization=request.user.organization,
            staff=staff,
            date=today,
            defaults={
                'check_in': now,
                'expected_time': staff.profile_data.get('work_start', '09:00'),
            }
        )
        if not created:
            messages.info(request, f"{staff.full_name} allaqachon kelgan")
        else:
            att.calculate_late_minutes()
            att.save()
            messages.success(request, f"{staff.full_name} keldi ({now.strftime('%H:%M')})")
        return redirect('staff_attendance_list')
    return redirect('staff_attendance_list')
@login_required
def staff_check_out(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id') or request.user.id
        staff = get_object_or_404(User, pk=staff_id, organization=request.user.organization)
        today = date.today()
        now = timezone.now().time()
        try:
            att = StaffAttendance.objects.get(
                organization=request.user.organization,
                staff=staff,
                date=today
            )
            att.check_out = now
            att.save()
            messages.success(request, f"{staff.full_name} ketdi ({now.strftime('%H:%M')})")
        except StaffAttendance.DoesNotExist:
            messages.error(request, f"{staff.full_name} bugun kelmagan")
        return redirect('staff_attendance_list')
    return redirect('staff_attendance_list')

--- apps\finance\services.py ---
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.finance.models import Transaction
@transaction.atomic
def confirm_transaction(transaction_id, user):
    try:
        tx = Transaction.objects.select_for_update().get(id=transaction_id)
    except Transaction.DoesNotExist:
        raise ValidationError("Tranzaksiya topilmadi.")
    if tx.status == 'confirmed':
        return tx
    if tx.transaction_type == 'income':
        tx.account.balance += tx.amount
    elif tx.transaction_type in ['expense', 'salary', 'refund']:
        if tx.account.balance < tx.amount:
            raise ValidationError(f"Kassada mablag' yetarli emas! Mavjud: {tx.account.balance}")
        tx.account.balance -= tx.amount
    tx.account.save()
    if tx.student and tx.transaction_type == 'income':
        tx.student.balance += tx.amount
        tx.student.save()
    tx.status = 'confirmed'
    tx.confirmed_by = user
    tx.confirmed_at = timezone.now()
    tx.receipt_verified = True
    tx.receipt_verified_by = user
    tx.receipt_verified_at = timezone.now()
    tx.save()
    return tx

--- apps\finance\urls.py ---
from django.urls import path
from . import views
from . import payroll_views
from . import inventory_views
app_name = 'finance'
urlpatterns = [
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_create'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/income/', views.add_income, name='add_income'),
    path('transactions/expense/', views.add_expense, name='add_expense'),
    path('transactions/<int:pk>/confirm/', views.confirm_transaction, name='confirm_transaction'),
    path('transactions/<int:pk>/reject/', views.reject_transaction, name='reject_transaction'),
    path('students/<int:student_id>/payments/', views.student_payments, name='student_payments'),
    path('students/<int:student_id>/payments/add/', views.add_student_payment, name='add_student_payment'),
    path('students/<int:student_id>/payment/', views.add_student_payment, name='student_payment'),
    path('reports/', views.finance_report, name='report'),
    path('payroll/', payroll_views.payroll_list, name='payroll_list'),
    path('payroll/<int:staff_id>/calculate/', payroll_views.calculate_payroll, name='calculate_payroll'),
    path('payroll/<int:pk>/approve/', payroll_views.approve_payroll, name='approve_payroll'),
    path('payroll/<int:pk>/pay/', payroll_views.pay_salary, name='pay_salary'),
    path('hr/attendance/', payroll_views.staff_attendance_list, name='staff_attendance_list'),
    path('hr/check-in/', payroll_views.staff_check_in, name='staff_check_in'),
    path('hr/check-out/', payroll_views.staff_check_out, name='staff_check_out'),
    path('supplies/', inventory_views.supply_list, name='supply_list'),
    path('supplies/<int:supply_id>/add/', inventory_views.supply_add_stock, name='supply_add_stock'),
    path('supplies/<int:supply_id>/remove/', inventory_views.supply_remove_stock, name='supply_remove_stock'),
    path('assets/', inventory_views.asset_list, name='asset_list'),
    path('receipts/pending/', views.pending_receipts, name='pending_receipts'),
    path('receipts/<int:pk>/verify/', views.verify_receipt, name='verify_receipt'),
    path('receipts/<int:pk>/reject/', views.reject_receipt, name='reject_receipt'),
]

--- apps\finance\views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import timedelta
from .models import Account, Transaction, TransactionCategory
from apps.core.audit import log_user_action
@login_required
def transaction_list(request):
    org = request.organization
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    trans_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    account_id = request.GET.get('account', '')
    transactions = Transaction.objects.filter(is_deleted=False)
    if org:
        transactions = transactions.filter(organization=org)
    if date_from:
        transactions = transactions.filter(created_at__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(created_at__date__lte=date_to)
    if trans_type:
        transactions = transactions.filter(transaction_type=trans_type)
    if status:
        transactions = transactions.filter(status=status)
    if account_id:
        transactions = transactions.filter(account_id=account_id)
    stats_qs = transactions.filter(status='confirmed')
    income = stats_qs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or 0
    expense = stats_qs.filter(transaction_type='expense').aggregate(t=Sum('amount'))['t'] or 0
    transactions = transactions.select_related(
        'account', 'category', 'student', 'staff', 'created_by', 'confirmed_by'
    ).order_by('-created_at')[:100]
    accounts = Account.objects.filter(is_deleted=False)
    if org:
        accounts = accounts.filter(organization=org)
    context = {
        'transactions': transactions,
        'accounts': accounts,
        'income': income,
        'expense': expense,
        'balance': income - expense,
        'date_from': date_from,
        'date_to': date_to,
        'trans_type': trans_type,
        'status': status,
        'account_id': account_id,
    }
    return render(request, 'finance/transaction_list.html', context)
@login_required
def account_list(request):
    org = request.organization
    accounts = Account.objects.filter(is_deleted=False)
    if org:
        accounts = accounts.filter(organization=org)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    return render(request, 'finance/account_list.html', {'accounts': accounts, 'total_balance': total_balance})
@login_required
def account_create(request):
    from .forms import AccountForm
    org = request.organization
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.organization = org
            acc.save()
            messages.success(request, "Kassa yaratildi")
            return redirect('finance:account_list')
    else:
        form = AccountForm()
    return render(request, 'finance/account_form.html', {'form': form, 'title': 'Yangi Kassa'})
@login_required
def add_income(request):
    from .forms import TransactionForm
    org = request.organization
    if request.method == 'POST':
        form = TransactionForm(request.POST, organization=org, transaction_type='income')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.transaction_type = 'income'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "Kirim qo'shildi")
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm(organization=org, transaction_type='income')
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Kirim', 'type': 'income'})
@login_required
def add_expense(request):
    from .forms import TransactionForm
    org = request.organization
    if request.method == 'POST':
        form = TransactionForm(request.POST, organization=org, transaction_type='expense')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.transaction_type = 'expense'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "Chiqim qo'shildi")
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm(organization=org, transaction_type='expense')
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Chiqim', 'type': 'expense'})
@login_required
def confirm_transaction(request, pk):
    from .services import confirm_transaction as confirm_service
    try:
        confirm_service(pk, request.user)
        messages.success(request, "Tasdiqlandi")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('finance:transaction_list')
@login_required
def reject_transaction(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    if t.status == 'pending':
        t.status = 'rejected'
        t.save()
        messages.warning(request, "Rad etildi")
    return redirect('finance:transaction_list')
@login_required
def student_payments(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    payments = Transaction.objects.filter(student=student).order_by('-created_at')
    total = payments.filter(transaction_type='income', status='confirmed').aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'finance/student_payments.html', {'student': student, 'payments': payments, 'total_paid': total})
@login_required
def add_student_payment(request, student_id):
    from .forms import StudentPaymentForm
    student = get_object_or_404(User, pk=student_id)
    if request.method == 'POST':
        form = StudentPaymentForm(request.POST, request.FILES, organization=request.organization)
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = request.organization
            t.student = student
            t.transaction_type = 'income'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "To'lov qabul qilindi")
            return redirect('finance:student_payments', student_id=student.id)
    else:
        form = StudentPaymentForm(organization=request.organization)
    return render(request, 'finance/student_payment_form.html', {'form': form, 'student': student})
@login_required
def finance_report(request):
    return render(request, 'finance/report.html', {})
@login_required
def pending_receipts(request):
    txs = Transaction.objects.filter(receipt_verified=False, status='pending')
    return render(request, 'finance/pending_receipts.html', {'pending_receipts': txs})
@login_required
def verify_receipt(request, pk):
    return confirm_transaction(request, pk)
@login_required
def reject_receipt(request, pk):
    return reject_transaction(request, pk)

--- apps\operations\admin.py ---
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Lesson, Attendance
from .services import finish_lesson_logic
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ['student']
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'start_time', 'teacher', 'status')
    list_filter = ('status', 'date', 'group')
    inlines = [AttendanceInline]
    change_list_template = "admin/operations/lesson/change_list.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:lesson_id>/finish/', self.admin_site.admin_view(self.finish_lesson_view), name='lesson-finish'),
        ]
        return custom_urls + urls
    def finish_lesson_view(self, request, lesson_id):
        try:
            msg = finish_lesson_logic(lesson_id, request.user)
            self.message_user(request, msg, level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Xatolik: {e}", level=messages.ERROR)
        return redirect('admin:operations_lesson_changelist')

--- apps\operations\apps.py ---
from django.apps import AppConfig
class OperationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.operations'
    verbose_name = "Kundalik Operatsiyalar"

--- apps\operations\gamification.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
class Level(TenantAwareModel):
    name = models.CharField(max_length=50, verbose_name="Daraja nomi")
    name_uz = models.CharField(max_length=50, verbose_name="O'zbekcha nomi")
    min_xp = models.PositiveIntegerField(verbose_name="Minimal XP")
    max_xp = models.PositiveIntegerField(verbose_name="Maksimal XP")
    icon = models.CharField(max_length=50, default='⭐', verbose_name="Ikonka")
    color = models.CharField(max_length=20, default='blue', verbose_name="Rang")
    class Meta:
        db_table = 'gamification_levels'
        ordering = ['min_xp']
        verbose_name = "Daraja"
        verbose_name_plural = "Darajalar"
    def __str__(self):
        return f"{self.name} ({self.min_xp}-{self.max_xp} XP)"
class Badge(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Nishon nomi")
    description = models.CharField(max_length=255, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='🏆', verbose_name="Ikonka")
    color = models.CharField(max_length=20, default='yellow', verbose_name="Rang")
    TRIGGER_CHOICES = (
        ('attendance_streak', 'Ketma-ket davomat'),
        ('grade_average', "O'rtacha baho"),
        ('xp_milestone', 'XP chegara'),
        ('lessons_count', 'Darslar soni'),
        ('manual', 'Qo\'lda beriladi'),
    )
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_CHOICES, default='manual', verbose_name="Trigger turi")
    trigger_value = models.PositiveIntegerField(default=0, verbose_name="Trigger qiymati")
    xp_reward = models.PositiveIntegerField(default=0, verbose_name="XP mukofoti")
    class Meta:
        db_table = 'gamification_badges'
        verbose_name = "Nishon"
        verbose_name_plural = "Nishonlar"
    def __str__(self):
        return f"{self.icon} {self.name}"
class StudentBadge(TenantAwareModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges',
                               limit_choices_to={'role': 'student'})
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_to')
    awarded_at = models.DateTimeField(auto_now_add=True)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='awarded_badges')
    notes = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'student_badges'
        ordering = ['-awarded_at']
        verbose_name = "O'quvchi nishoni"
        verbose_name_plural = "O'quvchi nishonlari"
        unique_together = ('student', 'badge')
    def __str__(self):
        return f"{self.student.full_name} - {self.badge.name}"
class XPTransaction(TenantAwareModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_transactions',
                               limit_choices_to={'role': 'student'})
    SOURCE_CHOICES = (
        ('attendance', 'Davomat'),
        ('grade', 'Baho'),
        ('badge', 'Nishon'),
        ('bonus', 'Bonus'),
        ('penalty', 'Jarima'),
    )
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, verbose_name="Manba")
    amount = models.IntegerField(verbose_name="XP miqdori")
    description = models.CharField(max_length=255, blank=True)
    related_lesson = models.ForeignKey('operations.Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'xp_transactions'
        ordering = ['-created_at']
        verbose_name = "XP harakati"
        verbose_name_plural = "XP harakatlari"
    def __str__(self):
        sign = '+' if self.amount > 0 else ''
        return f"{self.student.full_name}: {sign}{self.amount} XP ({self.source})"
    def save(self, *args, **kwargs):
        if self._state.adding:
            from apps.users.models import User
            xp_data = self.student.profile_data.get('xp', 0)
            self.student.profile_data['xp'] = max(0, xp_data + self.amount)
            self.student.save(update_fields=['profile_data'])
        super().save(*args, **kwargs)
class Streak(TenantAwareModel):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak',
                                   limit_choices_to={'role': 'student'})
    current_streak = models.PositiveIntegerField(default=0, verbose_name="Joriy streak")
    longest_streak = models.PositiveIntegerField(default=0, verbose_name="Eng uzun streak")
    last_attendance_date = models.DateField(null=True, blank=True, verbose_name="Oxirgi davomat")
    class Meta:
        db_table = 'student_streaks'
        verbose_name = "O'quvchi streak"
        verbose_name_plural = "O'quvchi streaklari"
    def __str__(self):
        return f"{self.student.full_name}: {self.current_streak} kun"
    def update_streak(self, attendance_date):
        from datetime import timedelta
        if self.last_attendance_date:
            diff = (attendance_date - self.last_attendance_date).days
            if diff == 1:
                self.current_streak += 1
            elif diff > 1:
                self.current_streak = 1
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_attendance_date = attendance_date
        self.save()

--- apps\operations\models.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.education.models import Group, Room
from apps.operations.gamification import Level, Badge, StudentBadge, XPTransaction, Streak
from apps.operations.schedule import SchedulePattern, LessonGenerationLog
from apps.operations.shop import ShopCategory, ShopItem, Purchase
class Lesson(TenantAwareModel):
    STATUS_CHOICES = (
        ('scheduled', 'Rejalashtirilgan'),
        ('started', 'Dars ketmoqda'),
        ('finished', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons', verbose_name="Guruh")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="O'qituvchi")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, verbose_name="Xona")
    date = models.DateField(verbose_name="Sana")
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")
    topic = models.CharField(max_length=255, blank=True, verbose_name="Mavzu")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name="Holati")
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.group.name} ({self.date})"
    class Meta:
        db_table = 'lessons'
        ordering = ['-date', '-start_time']
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
class Attendance(TenantAwareModel):
    STATUS_CHOICES = (
        ('present', 'Bor'),
        ('absent', 'Yo\'q (Sababsiz)'),
        ('excused', 'Sababli'),
        ('late', 'Kechikdi'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_attendances')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    grade = models.PositiveIntegerField(null=True, blank=True, verbose_name="Baho (0-100)")
    xp_points = models.PositiveIntegerField(default=0, verbose_name="XP Ochko")
    comment = models.CharField(max_length=255, blank=True, verbose_name="Izoh")
    class Meta:
        db_table = 'attendance'
        unique_together = ('lesson', 'student')
        verbose_name = "Davomat"
        verbose_name_plural = "Davomatlar"

--- apps\operations\schedule.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.education.models import Group, Room
class SchedulePattern(TenantAwareModel):
    DAYS_OF_WEEK = (
        (0, 'Dushanba'),
        (1, 'Seshanba'),
        (2, 'Chorshanba'),
        (3, 'Payshanba'),
        (4, 'Juma'),
        (5, 'Shanba'),
        (6, 'Yakshanba'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedule_patterns', verbose_name="Guruh")
    day_of_week = models.PositiveIntegerField(choices=DAYS_OF_WEEK, verbose_name="Hafta kuni")
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='schedule_patterns', verbose_name="Xona")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    class Meta:
        db_table = 'schedule_patterns'
        ordering = ['day_of_week', 'start_time']
        verbose_name = "Jadval patterni"
        verbose_name_plural = "Jadval patternlari"
    def __str__(self):
        return f"{self.group.name} - {self.get_day_of_week_display()} {self.start_time}"
    @classmethod
    def check_room_conflict(cls, room, day_of_week, start_time, end_time, exclude_id=None):
        if not room:
            return False, None
        conflicts = cls.objects.filter(
            room=room,
            day_of_week=day_of_week,
            is_active=True
        )
        if exclude_id:
            conflicts = conflicts.exclude(id=exclude_id)
        for pattern in conflicts:
            if (start_time < pattern.end_time and end_time > pattern.start_time):
                return True, pattern
        return False, None
    @classmethod
    def check_teacher_conflict(cls, teacher, day_of_week, start_time, end_time, exclude_id=None):
        conflicts = cls.objects.filter(
            group__teacher=teacher,
            day_of_week=day_of_week,
            is_active=True
        )
        if exclude_id:
            conflicts = conflicts.exclude(id=exclude_id)
        for pattern in conflicts:
            if (start_time < pattern.end_time and end_time > pattern.start_time):
                return True, pattern
        return False, None
class LessonGenerationLog(TenantAwareModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='generation_logs')
    date_from = models.DateField(verbose_name="Boshlang'ich sana")
    date_to = models.DateField(verbose_name="Tugash sanasi")
    lessons_created = models.PositiveIntegerField(default=0, verbose_name="Yaratilgan darslar")
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'lesson_generation_logs'
        ordering = ['-created_at']
        verbose_name = "Dars yaratish logi"
        verbose_name_plural = "Dars yaratish loglari"
def generate_lessons_for_group(group, date_from, date_to, created_by=None):
    from datetime import timedelta
    from apps.operations.models import Lesson
    patterns = SchedulePattern.objects.filter(group=group, is_active=True)
    if not patterns.exists():
        return 0
    lessons_created = 0
    current_date = date_from
    while current_date <= date_to:
        day_of_week = current_date.weekday()
        for pattern in patterns.filter(day_of_week=day_of_week):
            exists = Lesson.objects.filter(
                group=group,
                date=current_date,
                start_time=pattern.start_time
            ).exists()
            if not exists:
                Lesson.objects.create(
                    organization=group.organization,
                    group=group,
                    teacher=group.teacher,
                    room=pattern.room,
                    date=current_date,
                    start_time=pattern.start_time,
                    end_time=pattern.end_time,
                    status='scheduled'
                )
                lessons_created += 1
        current_date += timedelta(days=1)
    if lessons_created > 0:
        LessonGenerationLog.objects.create(
            organization=group.organization,
            group=group,
            date_from=date_from,
            date_to=date_to,
            lessons_created=lessons_created,
            generated_by=created_by
        )
    return lessons_created

--- apps\operations\services.py ---
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.operations.models import Lesson, Attendance
from apps.finance.models import Transaction, Account, TransactionCategory
from apps.users.models import User
@transaction.atomic
def finish_lesson_logic(lesson_id, user):
    try:
        lesson = Lesson.objects.select_for_update().get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ValidationError("Dars topilmadi")
    if lesson.status == 'finished':
        raise ValidationError("Bu dars allaqachon yakunlangan va pullar yechilgan.")
    lesson_price = 50000
    if lesson.group.course.price > 0:
        lesson_price = lesson.group.course.price / 12
    category, _ = TransactionCategory.objects.get_or_create(
        organization=lesson.organization,
        transaction_type='income',
        defaults={'name': 'Kurs to\'lovi avtomat'}
    )
    attendances = Attendance.objects.filter(lesson=lesson)
    if not attendances.exists():
        raise ValidationError("Davomat qilinmagan! Avval o'quvchilarni belgilang.")
    for att in attendances:
        if att.status in ['present', 'late', 'absent']:
            Transaction.objects.create(
                organization=lesson.organization,
                branch=lesson.group.room.organization.branches.first() if lesson.room else None,
                account=Account.objects.filter(organization=lesson.organization).first(),
                category=category,
                student=att.student,
                amount=lesson_price,
                transaction_type='income',
                status='confirmed',
                created_by=user,
                confirmed_by=user,
                confirmed_at=timezone.now(),
                description=f"{lesson.group.name} - {lesson.date} darsi uchun to'lov"
            )
            att.student.balance -= lesson_price
            att.student.save()
    lesson.status = 'finished'
    lesson.finished_at = timezone.now()
    lesson.save()
    return "Dars yakunlandi va hisob-kitob qilindi."

--- apps\operations\shop.py ---
from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.finance.inventory import Supply
class ShopCategory(TenantAwareModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    icon = models.CharField(max_length=50, default='🎁', verbose_name="Ikonka")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    class Meta:
        db_table = 'shop_categories'
        ordering = ['order', 'name']
        verbose_name = "Do'kon kategoriyasi"
        verbose_name_plural = "Do'kon kategoriyalari"
    def __str__(self):
        return f"{self.icon} {self.name}"
class ShopItem(TenantAwareModel):
    category = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='items', verbose_name="Kategoriya")
    name = models.CharField(max_length=200, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    coin_price = models.PositiveIntegerField(default=100, verbose_name="Coin narxi")
    supply = models.ForeignKey(Supply, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='shop_items', verbose_name="Sklad mahsuloti")
    stock = models.PositiveIntegerField(default=0, verbose_name="Mavjud soni")
    image = models.ImageField(upload_to='shop/%Y/%m/', null=True, blank=True, verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    class Meta:
        db_table = 'shop_items'
        ordering = ['-is_featured', 'category', 'name']
        verbose_name = "Do'kon mahsuloti"
        verbose_name_plural = "Do'kon mahsulotlari"
    def __str__(self):
        return f"{self.name} ({self.coin_price} 💰)"
    @property
    def available_stock(self):
        if self.supply:
            return self.supply.quantity
        return self.stock
    @property
    def is_in_stock(self):
        return self.available_stock > 0 and self.is_active
class Purchase(TenantAwareModel):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('delivered', 'Topshirildi'),
        ('cancelled', 'Bekor qilindi'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases',
                                limit_choices_to={'role': 'student'}, verbose_name="O'quvchi")
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name='purchases',
                             verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    coin_spent = models.PositiveIntegerField(verbose_name="Sarflangan coin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                              verbose_name="Holati")
    delivered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='delivered_purchases', verbose_name="Topshirdi")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Topshirilgan vaqt")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    class Meta:
        db_table = 'shop_purchases'
        ordering = ['-created_at']
        verbose_name = "Xarid"
        verbose_name_plural = "Xaridlar"
    def __str__(self):
        return f"{self.student.first_name} - {self.item.name}"
    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.coin_spent:
                self.coin_spent = self.item.coin_price * self.quantity
            xp_data = self.student.profile_data.get('xp', 0)
            if xp_data >= self.coin_spent:
                self.student.profile_data['xp'] = xp_data - self.coin_spent
                self.student.save(update_fields=['profile_data'])
            if self.item.supply:
                self.item.supply.quantity = max(0, self.item.supply.quantity - self.quantity)
                self.item.supply.save()
            else:
                self.item.stock = max(0, self.item.stock - self.quantity)
                self.item.save()
        super().save(*args, **kwargs)

--- apps\operations\shop_views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from apps.operations.shop import ShopCategory, ShopItem, Purchase
from apps.users.models import User
from apps.core.audit import log_user_action
@login_required
def shop_list(request):
    org = request.organization
    categories = ShopCategory.objects.filter(organization=org, is_deleted=False)
    items = ShopItem.objects.filter(
        organization=org,
        is_deleted=False,
        is_active=True
    ).select_related('category', 'supply')
    featured = items.filter(is_featured=True)[:4]
    user_coins = request.user.profile_data.get('xp', 0)
    context = {
        'categories': categories,
        'items': items,
        'featured': featured,
        'user_coins': user_coins,
    }
    return render(request, 'operations/shop.html', context)
@login_required
def purchase_item(request, item_id):
    org = request.organization
    item = get_object_or_404(ShopItem, pk=item_id, organization=org, is_active=True)
    if request.user.role != 'student':
        messages.error(request, "Faqat o'quvchilar sotib olishi mumkin!")
        return redirect('operations:shop')
    user_coins = request.user.profile_data.get('xp', 0)
    if user_coins < item.coin_price:
        messages.error(request, f"Yetarli coin yo'q! Sizda: {user_coins} 💰, Kerak: {item.coin_price} 💰")
        return redirect('operations:shop')
    if not item.is_in_stock:
        messages.error(request, "Bu mahsulot tugagan!")
        return redirect('operations:shop')
    purchase = Purchase.objects.create(
        organization=org,
        student=request.user,
        item=item,
        quantity=1,
        coin_spent=item.coin_price,
        status='pending'
    )
    log_user_action(request.user, 'CREATE', 'Purchase', purchase.id,
                   f"Do'kondan sotib oldi: {item.name}", request=request)
    messages.success(request, f"✅ {item.name} muvaffaqiyatli sotib olindi! Admindan olib keting.")
    return redirect('operations:shop')
@login_required
def purchase_history(request):
    org = request.organization
    if request.user.role == 'student':
        purchases = Purchase.objects.filter(
            organization=org,
            student=request.user,
            is_deleted=False
        ).select_related('item')
    else:
        purchases = Purchase.objects.filter(
            organization=org,
            is_deleted=False
        ).select_related('item', 'student')
    total_spent = purchases.filter(status__in=['pending', 'delivered']).aggregate(
        total=Sum('coin_spent')
    )['total'] or 0
    context = {
        'purchases': purchases[:50],
        'total_spent': total_spent,
    }
    return render(request, 'operations/purchase_history.html', context)
@login_required
def shop_admin(request):
    org = request.organization
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('operations:shop')
    items = ShopItem.objects.filter(organization=org, is_deleted=False).select_related('category', 'supply')
    categories = ShopCategory.objects.filter(organization=org, is_deleted=False)
    pending_purchases = Purchase.objects.filter(
        organization=org,
        status='pending',
        is_deleted=False
    ).select_related('student', 'item')
    context = {
        'items': items,
        'categories': categories,
        'pending_purchases': pending_purchases,
        'pending_count': pending_purchases.count(),
    }
    return render(request, 'operations/shop_admin.html', context)
@login_required
def deliver_purchase(request, pk):
    org = request.organization
    purchase = get_object_or_404(Purchase, pk=pk, organization=org)
    if purchase.status == 'pending':
        purchase.status = 'delivered'
        purchase.delivered_by = request.user
        purchase.delivered_at = timezone.now()
        purchase.save()
        log_user_action(request.user, 'UPDATE', 'Purchase', purchase.id,
                       f"Topshirildi: {purchase.item.name}", request=request)
        messages.success(request, f"✅ {purchase.item.name} topshirildi!")
    return redirect('operations:shop_admin')
@login_required
def cancel_purchase(request, pk):
    org = request.organization
    purchase = get_object_or_404(Purchase, pk=pk, organization=org)
    if purchase.status == 'pending':
        xp_data = purchase.student.profile_data.get('xp', 0)
        purchase.student.profile_data['xp'] = xp_data + purchase.coin_spent
        purchase.student.save(update_fields=['profile_data'])
        if purchase.item.supply:
            purchase.item.supply.quantity += purchase.quantity
            purchase.item.supply.save()
        else:
            purchase.item.stock += purchase.quantity
            purchase.item.save()
        purchase.status = 'cancelled'
        purchase.save()
        log_user_action(request.user, 'UPDATE', 'Purchase', purchase.id,
                       f"Bekor qilindi: {purchase.item.name}", request=request)
        messages.warning(request, f"Xarid bekor qilindi. {purchase.coin_spent} coin qaytarildi.")
    return redirect('operations:shop_admin')

--- apps\operations\urls.py ---
from django.urls import path
from . import views
from . import shop_views
app_name = 'operations'
urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:pk>/start/', views.start_lesson, name='start_lesson'),
    path('lessons/<int:pk>/finish/', views.finish_lesson, name='finish_lesson'),
    path('lessons/<int:pk>/attendance/', views.take_attendance, name='take_attendance'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('ratings/teachers/', views.teacher_ratings, name='teacher_ratings'),
    path('ratings/students/', views.student_ratings, name='student_ratings'),
    path('shop/', shop_views.shop_list, name='shop'),
    path('shop/buy/<int:item_id>/', shop_views.purchase_item, name='purchase_item'),
    path('shop/history/', shop_views.purchase_history, name='purchase_history'),
    path('shop/admin/', shop_views.shop_admin, name='shop_admin'),
    path('shop/deliver/<int:pk>/', shop_views.deliver_purchase, name='deliver_purchase'),
    path('shop/cancel/<int:pk>/', shop_views.cancel_purchase, name='cancel_purchase'),
]

--- apps\operations\views.py ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Avg
from datetime import timedelta
from .models import Lesson, Attendance
from apps.education.models import Group, GroupStudent
from apps.users.models import User
from apps.core.audit import log_user_action
@login_required
def lesson_list(request):
    org = request.user.organization
    user = request.user
    today = timezone.now().date()
    date_filter = request.GET.get('date', str(today))
    group_filter = request.GET.get('group', '')
    status_filter = request.GET.get('status', '')
    lessons = Lesson.objects.filter(organization=org, is_deleted=False)
    if user.role == 'teacher':
        lessons = lessons.filter(teacher=user)
    if date_filter:
        lessons = lessons.filter(date=date_filter)
    if group_filter:
        lessons = lessons.filter(group_id=group_filter)
    if status_filter:
        lessons = lessons.filter(status=status_filter)
    lessons = lessons.select_related('group', 'teacher', 'room').order_by('start_time')
    if user.role == 'teacher':
        groups = Group.objects.filter(teacher=user, is_deleted=False)
    else:
        groups = Group.objects.filter(organization=org, is_deleted=False)
    context = {
        'lessons': lessons,
        'groups': groups,
        'today': today,
        'date_filter': date_filter,
        'group_filter': group_filter,
        'status_filter': status_filter,
    }
    return render(request, 'operations/lesson_list.html', context)
@login_required
def lesson_detail(request, pk):
    org = request.user.organization
    lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)
    attendances = Attendance.objects.filter(lesson=lesson).select_related('student')
    context = {
        'lesson': lesson,
        'attendances': attendances,
    }
    return render(request, 'operations/lesson_detail.html', context)
@login_required
def start_lesson(request, pk):
    org = request.user.organization
    lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)
    if lesson.status == 'scheduled':
        lesson.status = 'started'
        lesson.started_at = timezone.now()
        lesson.save()
        log_user_action(request.user, 'UPDATE', 'Lesson', lesson.id, str(lesson),
                       changes={'status': 'started'}, request=request)
        messages.success(request, "Dars boshlandi!")
    return redirect('take_attendance', pk=lesson.pk)
@login_required
def finish_lesson(request, pk):
    org = request.user.organization
    lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)
    if lesson.status in ['scheduled', 'started']:
        lesson.status = 'finished'
        lesson.finished_at = timezone.now()
        lesson.save()
        log_user_action(request.user, 'UPDATE', 'Lesson', lesson.id, str(lesson),
                       changes={'status': 'finished'}, request=request)
        messages.success(request, "Dars yakunlandi!")
    return redirect('lesson_list')
@login_required
def take_attendance(request, pk):
    org = request.user.organization
    lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)
    group_students = GroupStudent.objects.filter(
        group=lesson.group,
        status='active'
    ).select_related('student')
    existing_attendances = {
        att.student_id: att
        for att in Attendance.objects.filter(lesson=lesson)
    }
    if request.method == 'POST':
        for gs in group_students:
            student = gs.student
            status = request.POST.get(f'status_{student.id}', 'absent')
            grade = request.POST.get(f'grade_{student.id}', '')
            comment = request.POST.get(f'comment_{student.id}', '')
            xp = 0
            if status == 'present':
                xp = 10
            elif status == 'late':
                xp = 5
            elif status == 'excused':
                xp = 3
            if student.id in existing_attendances:
                att = existing_attendances[student.id]
                att.status = status
                att.grade = int(grade) if grade else None
                att.comment = comment
                att.xp_points = xp
                att.save()
            else:
                Attendance.objects.create(
                    organization=org,
                    lesson=lesson,
                    student=student,
                    status=status,
                    grade=int(grade) if grade else None,
                    comment=comment,
                    xp_points=xp,
                )
        log_user_action(request.user, 'UPDATE', 'Attendance', lesson.id,
                       f"Davomat - {lesson.group.name}", request=request)
        messages.success(request, "Davomat saqlandi!")
        return redirect('lesson_list')
    students_data = []
    for gs in group_students:
        existing = existing_attendances.get(gs.student_id)
        students_data.append({
            'student': gs.student,
            'status': existing.status if existing else 'present',
            'grade': existing.grade if existing else None,
            'comment': existing.comment if existing else '',
        })
    context = {
        'lesson': lesson,
        'students_data': students_data,
    }
    return render(request, 'operations/take_attendance.html', context)
@login_required
def schedule_view(request):
    org = request.user.organization
    user = request.user
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    week_offset = int(request.GET.get('week', 0))
    start_of_week += timedelta(weeks=week_offset)
    end_of_week += timedelta(weeks=week_offset)
    lessons = Lesson.objects.filter(
        organization=org,
        date__range=[start_of_week, end_of_week],
        is_deleted=False
    )
    if user.role == 'teacher':
        lessons = lessons.filter(teacher=user)
    elif user.role == 'student':
        my_groups = GroupStudent.objects.filter(
            student=user, status='active'
        ).values_list('group_id', flat=True)
        lessons = lessons.filter(group_id__in=my_groups)
    lessons = lessons.select_related('group', 'teacher', 'room').order_by('date', 'start_time')
    week_days = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_lessons = [l for l in lessons if l.date == day]
        week_days.append({
            'date': day,
            'is_today': day == today,
            'lessons': day_lessons,
        })
    context = {
        'week_days': week_days,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_offset': week_offset,
        'today': today,
    }
    return render(request, 'operations/schedule.html', context)
@login_required
def teacher_ratings(request):
    org = request.user.organization
    teachers = User.objects.filter(
        organization=org,
        role='teacher',
        is_active=True,
        is_deleted=False
    ).annotate(
        group_count=Count('teaching_groups', filter=Q(teaching_groups__status='active')),
        student_count=Count(
            'teaching_groups__students',
            filter=Q(teaching_groups__status='active', teaching_groups__students__status='active')
        ),
        lesson_count=Count('lesson', filter=Q(lesson__status='finished')),
    ).order_by('-student_count')
    teachers_data = []
    for teacher in teachers:
        total_att = Attendance.objects.filter(
            lesson__teacher=teacher,
            lesson__status='finished'
        ).count()
        present_att = Attendance.objects.filter(
            lesson__teacher=teacher,
            lesson__status='finished',
            status='present'
        ).count()
        att_rate = (present_att / total_att * 100) if total_att > 0 else 0
        avg_grade = Attendance.objects.filter(
            lesson__teacher=teacher,
            grade__isnull=False
        ).aggregate(avg=Avg('grade'))['avg'] or 0
        teachers_data.append({
            'teacher': teacher,
            'group_count': teacher.group_count,
            'student_count': teacher.student_count,
            'lesson_count': teacher.lesson_count,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
        })
    return render(request, 'operations/teacher_ratings.html', {'teachers_data': teachers_data})
@login_required
def student_ratings(request):
    org = request.user.organization
    students = User.objects.filter(
        organization=org,
        role='student',
        is_active=True,
        is_deleted=False
    )
    students_data = []
    for student in students:
        total_att = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='present').count()
        att_rate = (present / total_att * 100) if total_att > 0 else 0
        avg_grade = Attendance.objects.filter(
            student=student,
            grade__isnull=False
        ).aggregate(avg=Avg('grade'))['avg'] or 0
        total_xp = Attendance.objects.filter(student=student).aggregate(
            total=Count('xp_points')
        )['total'] or 0
        group_count = GroupStudent.objects.filter(
            student=student, status='active'
        ).count()
        students_data.append({
            'student': student,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
            'total_xp': total_xp,
            'group_count': group_count,
            'score': round(att_rate * 0.3 + avg_grade * 0.5 + total_xp * 0.2, 1)
        })
    students_data.sort(key=lambda x: x['score'], reverse=True)
    for i, data in enumerate(students_data):
        data['rank'] = i + 1
    return render(request, 'operations/student_ratings.html', {'students_data': students_data})

--- apps\organizations\admin.py ---
from django.contrib import admin
from .models import Organization, Branch
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'owner', 'is_active', 'created_at')
    search_fields = ('name', 'subdomain')
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'phone', 'is_main')
    list_filter = ('organization',)

--- apps\organizations\apps.py ---
from django.apps import AppConfig
class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.organizations'

--- apps\organizations\models.py ---
from django.db import models
from apps.core.models import BaseModel, SoftDeleteModel
class Organization(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name="Markaz nomi")
    subdomain = models.CharField(max_length=50, unique=True, verbose_name="Subdomain")
    owner = models.OneToOneField(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_organization',
        verbose_name="Markaz Egasi (Direktor)"
    )
    config = models.JSONField(default=dict, blank=True, verbose_name="Tizim Sozlamalari")
    is_active = models.BooleanField(default=True, verbose_name="Aktivmi?")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'organizations'
        verbose_name = "Tashkilot"
        verbose_name_plural = "Tashkilotlar"
class Branch(SoftDeleteModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255, verbose_name="Filial nomi")
    address = models.TextField(blank=True, verbose_name="Manzil")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    settings = models.JSONField(default=dict, blank=True, verbose_name="Filial Sozlamalari")
    is_main = models.BooleanField(default=False, verbose_name="Bosh filialmi?")
    def __str__(self):
        return f"{self.name} ({self.organization.name})"
    class Meta:
        db_table = 'branches'
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"

--- apps\users\admin.py ---
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ParentStudent
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('phone',)
    list_display = ('phone', 'first_name', 'last_name', 'role', 'organization', 'balance')
    list_filter = ('role', 'organization', 'is_active')
    search_fields = ('phone', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Shaxsiy ma\'lumotlar', {'fields': ('first_name', 'last_name', 'middle_name', 'avatar')}),
        ('Tizim', {'fields': ('role', 'organization', 'branch', 'is_active')}),
        ('Moliya & HR', {'fields': ('balance', 'nfc_card_id', 'profile_data')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'role', 'password'),
        }),
    )
@admin.register(ParentStudent)
class ParentStudentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'relation_type', 'is_main_contact')

--- apps\users\forms.py ---
from django import forms
from apps.users.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Parol")
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'role', 'branch', 'password', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ismi', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyasi', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '998901234567', 'required': True}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

--- apps\users\managers.py ---
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Telefon raqam kiritilishi shart')
        phone = ''.join(filter(str.isdigit, str(phone)))
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'super_admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)

--- apps\users\models.py ---
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import TenantAwareModel
from .managers import CustomUserManager
class User(AbstractUser, TenantAwareModel):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('owner', 'Direktor'),
        ('admin', 'Administrator'),
        ('teacher', 'O\'qituvchi'),
        ('student', 'O\'quvchi'),
        ('parent', 'Ota-ona'),
        ('staff', 'Xodim'),
    )
    username = None
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqam")
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram ID")
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Roli")
    branch = models.ForeignKey('organizations.Branch', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Filial")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Otasining ismi")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name="Rasm")
    nfc_card_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="NFC ID (Turniket)")
    profile_data = models.JSONField(default=dict, blank=True, verbose_name="Qo'shimcha Info")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Hisob (Balans)")
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}"
        return f"{full_name.strip()} ({self.phone})" if full_name.strip() else self.phone
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        db_table = 'users'
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
class ParentStudent(TenantAwareModel):
    RELATION_TYPES = (
        ('father', 'Otasi'),
        ('mother', 'Onasi'),
        ('guardian', 'Vasiysi'),
        ('relative', 'Qarindoshi'),
    )
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children_relations',
                               limit_choices_to={'role': 'parent'})
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_relations',
                                limit_choices_to={'role': 'student'})
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES, default='mother',
                                     verbose_name="Qarindoshligi")
    is_main_contact = models.BooleanField(default=False, verbose_name="Asosiy aloqa uchunmi?")
    class Meta:
        db_table = 'parent_student_relations'
        unique_together = ('parent', 'student')
        verbose_name = "Ota-ona bog'liqligi"
        verbose_name_plural = "Ota-ona bog'liqliklari"

--- apps\users\services.py ---
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
def compress_avatar(avatar):
    if not avatar:
        return avatar
    im = Image.open(avatar)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > 800:
        output_size = (800, 800)
        im.thumbnail(output_size)
    output = BytesIO()
    im.save(output, format='JPEG', quality=70)
    output.seek(0)
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{avatar.name.split('.')[0]}.jpg",
        'image/jpeg',
        sys.getsizeof(output),
        None
    )

--- apps\users\urls.py ---
from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('add/', views.user_create, name='user_create'),
    path('<int:pk>/edit/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
]

--- apps\users\views.py ---
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import User
from .forms import UserForm
@login_required
def user_list(request):
    users = User.objects.filter(is_deleted=False).select_related('organization', 'branch').order_by('-date_joined')
    if request.user.role != 'super_admin' and request.user.organization:
        users = users.filter(organization=request.user.organization)
    role = request.GET.get('role')
    if role:
        users = users.filter(role=role)
    filter_type = request.GET.get('filter')
    if filter_type == 'debtors':
        users = users.filter(role='student', balance__lt=0)
    search = request.GET.get('q')
    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    base_qs = User.objects.filter(is_deleted=False)
    if request.user.role != 'super_admin' and request.user.organization:
        base_qs = base_qs.filter(organization=request.user.organization)
    total_students = base_qs.filter(role='student', is_active=True).count()
    debtors_count = base_qs.filter(role='student', balance__lt=0).count()
    debt_agg = base_qs.filter(role='student', balance__lt=0).aggregate(total=Sum('balance'))
    total_debt = abs(debt_agg['total'] or 0)
    paginator = Paginator(users, 25)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    context = {
        'users': users_page,
        'total_students': total_students,
        'debtors_count': debtors_count,
        'total_debt': total_debt,
        'current_role': role,
        'current_filter': filter_type,
        'current_search': search,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'users/user_list.html', context)
@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.organization and request.user.organization:
                user.organization = request.user.organization
            user.save()
            messages.success(request, f"{user.first_name} muvaffaqiyatli qo'shildi!")
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': "Yangi foydalanuvchi"})
@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar yangilandi.")
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': "Tahrirlash"})
@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.warning(request, "Foydalanuvchi o'chirildi.")
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

--- config\asgi.py ---
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
application = get_asgi_application()

--- config\celery.py ---
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'daily-database-backup': {
        'task': 'apps.core.tasks.backup_and_report',
        'schedule': crontab(hour=23, minute=59),
    },
}

--- config\urls.py ---
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import dashboard_view
from apps.core.export_views import export_transactions, api_chart_data, global_search
from django.contrib.auth.views import LogoutView, LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard_view, name='dashboard'),
    path('api/chart-data/', api_chart_data, name='api_chart_data'),
    path('api/search/', global_search, name='global_search'),
    path('export/transactions/', export_transactions, name='export_transactions'),
    path('users/', include('apps.users.urls')),
    path('edu/', include('apps.education.urls')),
    path('crm/', include('apps.crm.urls')),
    path('operations/', include('apps.operations.urls')),
    path('finance/', include('apps.finance.urls')),
    path('automation/', include('apps.automation.urls')),
    path('core/', include('apps.core.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

--- config\wsgi.py ---
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
application = get_wsgi_application()

--- config\settings\base.py ---
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'django-insecure-production-key-change-me'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'apps.api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'apps.core',
    'apps.organizations',
    'apps.users',
    'apps.education',
    'apps.crm',
    'apps.finance',
    'apps.operations',
    'apps.automation',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.TenantMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.tenant_context',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
CORS_ALLOW_ALL_ORIGINS = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
import mimetypes
mimetypes.add_type('application/javascript', '.js', True)
if DEBUG:
    import os
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

--- static\css\style.css ---
/* ============================================
SMART EDU - PREMIUM DARK BLUE THEME
Clean, Modern, Professional
============================================ */
:root {
/* Dark Blue Color Palette */
--navy-900: #0a1628;
--navy-800: #0f1f35;
--navy-700: #152642;
--navy-600: #1c3255;
--navy-500: #234069;
--navy-400: #3a5a8a;
--navy-300: #5a7faf;
--navy-200: #8faad4;
--navy-100: #c4d5ea;
--navy-50: #e8eff7;
/* Accent Colors */
--accent-blue: #3b82f6;
--accent-cyan: #06b6d4;
--accent-purple: #8b5cf6;
--accent-green: #10b981;
--accent-amber: #f59e0b;
--accent-rose: #f43f5e;
/* Text Colors */
--text-white: #ffffff;
--text-light: #e2e8f0;
--text-muted: #94a3b8;
--text-dim: #64748b;
/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
--shadow-glow: 0 0 20px rgba(59, 130, 246, 0.3);
/* Transitions */
--transition: 200ms ease;
}
/* ============================================
GLOBAL DARK THEME OVERRIDES
Force dark blue theme on all pages
============================================ */
/* Override white backgrounds */
.bg-white,
.bg-gray-50,
.bg-gray-100 {
background: var(--navy-800) !important;
}
/* Glass Panel Override - most critical */
.glass-panel {
background: linear-gradient(145deg, var(--navy-700), var(--navy-800)) !important;
border: 1px solid var(--navy-600) !important;
box-shadow: var(--shadow-md) !important;
}
/* Text color overrides */
.text-gray-800,
.text-gray-700,
.text-gray-900 {
color: var(--text-white) !important;
}
.text-gray-600,
.text-gray-500 {
color: var(--text-muted) !important;
}
.text-gray-400 {
color: var(--text-dim) !important;
}
/* Border overrides */
.border-white,
.border-gray-100,
.border-gray-200 {
border-color: var(--navy-600) !important;
}
/* Input overrides */
input:not([type="checkbox"]):not([type="radio"]),
select,
textarea {
background: var(--navy-800) !important;
border: 1px solid var(--navy-600) !important;
color: var(--text-white) !important;
border-radius: 10px;
}
input::placeholder,
textarea::placeholder {
color: var(--text-dim) !important;
}
input:focus,
select:focus,
textarea:focus {
border-color: var(--accent-blue) !important;
box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
outline: none !important;
}
/* Table overrides */
table thead {
background: var(--navy-700) !important;
}
table tbody tr {
background: var(--navy-800) !important;
}
table tbody tr:hover {
background: var(--navy-700) !important;
}
table th,
table td {
border-color: var(--navy-600) !important;
color: var(--text-light) !important;
}
/* Form labels */
label {
color: var(--text-light) !important;
}
/* ============================================
SCROLLBAR - Slim & Elegant
============================================ */
::-webkit-scrollbar {
width: 6px;
height: 6px;
}
::-webkit-scrollbar-track {
background: var(--navy-800);
}
::-webkit-scrollbar-thumb {
background: var(--navy-500);
border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
background: var(--accent-blue);
}
/* ============================================
CARD STYLES
============================================ */
.card {
background: linear-gradient(145deg, var(--navy-700), var(--navy-800));
border: 1px solid var(--navy-600);
border-radius: 16px;
padding: 1.5rem;
box-shadow: var(--shadow-md);
transition: all var(--transition);
}
.card:hover {
border-color: var(--accent-blue);
box-shadow: var(--shadow-glow);
transform: translateY(-2px);
}
/* Stat Cards */
.stat-card {
background: linear-gradient(145deg, var(--navy-700), var(--navy-800));
border: 1px solid var(--navy-600);
border-radius: 16px;
padding: 1.5rem;
position: relative;
overflow: hidden;
transition: all var(--transition);
}
.stat-card::before {
content: '';
position: absolute;
top: 0;
right: 0;
width: 100px;
height: 100px;
background: radial-gradient(circle, rgba(59, 130, 246, 0.1), transparent 70%);
border-radius: 50%;
transform: translate(30%, -30%);
}
.stat-card:hover {
border-color: var(--accent-blue);
box-shadow: var(--shadow-glow);
transform: translateY(-3px);
}
/* Premium Card with Gradient Border */
.premium-card {
background: var(--navy-800);
border-radius: 16px;
padding: 1.5rem;
position: relative;
z-index: 1;
}
.premium-card::before {
content: '';
position: absolute;
inset: -1px;
background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
border-radius: 17px;
z-index: -1;
opacity: 0.5;
transition: opacity var(--transition);
}
.premium-card:hover::before {
opacity: 1;
}
/* ============================================
BUTTON STYLES
============================================ */
.btn {
display: inline-flex;
align-items: center;
gap: 0.5rem;
padding: 0.625rem 1.25rem;
font-weight: 600;
font-size: 0.875rem;
border-radius: 10px;
border: none;
cursor: pointer;
transition: all var(--transition);
}
.btn-primary {
background: linear-gradient(135deg, var(--accent-blue), #2563eb);
color: white;
box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
}
.btn-primary:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
}
.btn-success {
background: linear-gradient(135deg, var(--accent-green), #059669);
color: white;
box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}
.btn-success:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
}
.btn-danger {
background: linear-gradient(135deg, var(--accent-rose), #dc2626);
color: white;
box-shadow: 0 4px 14px rgba(244, 63, 94, 0.4);
}
.btn-ghost {
background: transparent;
color: var(--text-muted);
border: 1px solid var(--navy-500);
}
.btn-ghost:hover {
background: var(--navy-600);
color: var(--text-white);
border-color: var(--accent-blue);
}
/* ============================================
TABLE STYLES
============================================ */
.table-dark {
width: 100%;
border-collapse: separate;
border-spacing: 0;
}
.table-dark thead {
background: var(--navy-700);
}
.table-dark th {
padding: 1rem;
text-align: left;
font-size: 0.75rem;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;
color: var(--text-muted);
border-bottom: 2px solid var(--navy-600);
}
.table-dark tbody tr {
background: var(--navy-800);
transition: all var(--transition);
}
.table-dark tbody tr:hover {
background: var(--navy-700);
}
.table-dark td {
padding: 1rem;
color: var(--text-light);
border-bottom: 1px solid var(--navy-700);
}
/* ============================================
INPUT STYLES
============================================ */
.input-dark {
width: 100%;
padding: 0.75rem 1rem;
background: var(--navy-800);
border: 1px solid var(--navy-600);
border-radius: 10px;
color: var(--text-white);
font-size: 0.875rem;
transition: all var(--transition);
}
.input-dark::placeholder {
color: var(--text-dim);
}
.input-dark:focus {
outline: none;
border-color: var(--accent-blue);
box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
/* ============================================
BADGE STYLES
============================================ */
.badge {
display: inline-flex;
align-items: center;
padding: 0.25rem 0.75rem;
font-size: 0.75rem;
font-weight: 600;
border-radius: 9999px;
}
.badge-blue {
background: rgba(59, 130, 246, 0.2);
color: #60a5fa;
border: 1px solid rgba(59, 130, 246, 0.3);
}
.badge-green {
background: rgba(16, 185, 129, 0.2);
color: #34d399;
border: 1px solid rgba(16, 185, 129, 0.3);
}
.badge-amber {
background: rgba(245, 158, 11, 0.2);
color: #fbbf24;
border: 1px solid rgba(245, 158, 11, 0.3);
}
.badge-rose {
background: rgba(244, 63, 94, 0.2);
color: #fb7185;
border: 1px solid rgba(244, 63, 94, 0.3);
}
.badge-purple {
background: rgba(139, 92, 246, 0.2);
color: #a78bfa;
border: 1px solid rgba(139, 92, 246, 0.3);
}
/* ============================================
SIDEBAR STYLES
============================================ */
.sidebar-dark {
background: linear-gradient(180deg, var(--navy-900), var(--navy-800));
border-right: 1px solid var(--navy-700);
}
.sidebar-link {
display: flex;
align-items: center;
gap: 0.75rem;
padding: 0.75rem 1rem;
color: var(--text-muted);
border-radius: 10px;
transition: all var(--transition);
text-decoration: none;
}
.sidebar-link:hover {
background: var(--navy-700);
color: var(--text-white);
}
.sidebar-link.active {
background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.1));
color: var(--accent-blue);
border-left: 3px solid var(--accent-blue);
}
.sidebar-link i {
font-size: 1.25rem;
width: 1.5rem;
text-align: center;
}
.sidebar-section {
padding: 0.5rem 1rem;
margin-top: 1.5rem;
font-size: 0.65rem;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.1em;
color: var(--text-dim);
}
/* ============================================
HEADER STYLES
============================================ */
.header-dark {
background: rgba(15, 31, 53, 0.95);
backdrop-filter: blur(10px);
border-bottom: 1px solid var(--navy-700);
}
/* ============================================
UTILITY CLASSES
============================================ */
.text-gradient {
background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}
.text-gradient-purple {
background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}
.glow-blue {
box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}
.glow-green {
box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
}
.glow-purple {
box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}
/* Hover Effects */
.hover-lift {
transition: transform var(--transition), box-shadow var(--transition);
}
.hover-lift:hover {
transform: translateY(-4px);
box-shadow: var(--shadow-lg);
}
.hover-glow:hover {
box-shadow: var(--shadow-glow);
}
/* Icon Containers */
.icon-box {
display: inline-flex;
align-items: center;
justify-content: center;
width: 2.5rem;
height: 2.5rem;
border-radius: 10px;
font-size: 1.25rem;
}
.icon-box-lg {
width: 3rem;
height: 3rem;
border-radius: 12px;
font-size: 1.5rem;
}
.icon-blue {
background: linear-gradient(135deg, var(--accent-blue), #2563eb);
color: white;
box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}
.icon-green {
background: linear-gradient(135deg, var(--accent-green), #059669);
color: white;
box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}
.icon-amber {
background: linear-gradient(135deg, var(--accent-amber), #d97706);
color: white;
box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
}
.icon-rose {
background: linear-gradient(135deg, var(--accent-rose), #dc2626);
color: white;
box-shadow: 0 4px 14px rgba(244, 63, 94, 0.3);
}
.icon-purple {
background: linear-gradient(135deg, var(--accent-purple), #7c3aed);
color: white;
box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3);
}
/* ============================================
ANIMATIONS
============================================ */
@keyframes fadeIn {
from {
opacity: 0;
transform: translateY(10px);
}
to {
opacity: 1;
transform: translateY(0);
}
}
@keyframes pulse-glow {
0%,
100% {
box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
}
50% {
box-shadow: 0 0 25px rgba(59, 130, 246, 0.6);
}
}
.animate-fadeIn {
animation: fadeIn 0.4s ease-out;
}
.animate-pulse-glow {
animation: pulse-glow 2s ease-in-out infinite;
}
/* ============================================
RESPONSIVE
============================================ */
@media (max-width: 768px) {
.card,
.stat-card {
padding: 1rem;
}
.btn {
padding: 0.5rem 1rem;
font-size: 0.813rem;
}
}
/* ============================================
ACCESSIBILITY
============================================ */
@media (prefers-reduced-motion: reduce) {
* {
animation-duration: 0.01ms !important;
transition-duration: 0.01ms !important;
}
}
.focus-visible:focus {
outline: 2px solid var(--accent-blue);
outline-offset: 2px;
}

--- templates\base.html ---
{% load static %}
<!DOCTYPE html>
<html lang="uz" x-data="{
darkMode: localStorage.getItem('darkMode') === 'true',
sidebarOpen: window.innerWidth >= 1024
}" :class="{ 'dark': darkMode }">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}Dashboard{% endblock %} | Smart Edu</title>
<link rel="icon" href="data:,">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script>
tailwind.config = {
darkMode: 'class',
theme: {
extend: {
fontFamily: { sans: ['Inter', 'sans-serif'] },
colors: {
primary: { 50: '#eff6ff', 100: '#dbeafe', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8' },
dark: { 800: '#1e293b', 900: '#0f172a' }
}
}
}
}
</script>
<style>
[x-cloak] {
display: none !important;
}
</style>
</head>
<body class="bg-[#0a1628] text-slate-100 font-sans antialiased overflow-hidden">
<div class="flex h-screen w-full">
<aside
class="flex-shrink-0 w-64 sidebar-dark flex flex-col transition-all duration-300 transform lg:transform-none z-50 absolute lg:relative h-full"
:class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
<div class="h-16 flex items-center justify-center border-b border-[#152642]">
<span class="text-xl font-bold text-gradient flex items-center gap-2">
<i class="ph-fill ph-graduation-cap text-2xl"></i>
Smart Edu
</span>
</div>
<div id="sidebar-nav" class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
{% include 'components/sidebar.html' %}
</div>
<script>
// Save sidebar scroll position
document.addEventListener('DOMContentLoaded', function () {
const sidebar = document.getElementById('sidebar-nav');
const savedPos = localStorage.getItem('sidebarScrollPos');
// Restore scroll position
if (savedPos && sidebar) {
sidebar.scrollTop = parseInt(savedPos);
}
// Save scroll position before navigation
sidebar.addEventListener('click', function (e) {
const link = e.target.closest('a');
if (link) {
localStorage.setItem('sidebarScrollPos', sidebar.scrollTop);
}
});
// Also save on scroll
sidebar.addEventListener('scroll', function () {
localStorage.setItem('sidebarScrollPos', sidebar.scrollTop);
});
});
</script>
<div class="p-4 border-t border-[#152642] bg-[#0f1f35]/50">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 text-white flex items-center justify-center font-bold shadow-lg shadow-blue-500/20">
{{ request.user.first_name|first }}
</div>
<div class="flex-1 min-w-0">
<p class="text-sm font-semibold text-white truncate">{{ request.user.first_name }}</p>
<p class="text-xs text-slate-400 truncate">{{ request.user.get_role_display }}</p>
</div>
<a href="{% url 'logout' %}"
class="text-slate-400 hover:text-red-400 transition p-2 hover:bg-red-500/10 rounded-lg">
<i class="ph-fill ph-sign-out text-xl"></i>
</a>
</div>
</div>
</aside>
<div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
<header class="h-16 header-dark flex items-center justify-between px-6 z-40">
<button @click="sidebarOpen = !sidebarOpen"
class="text-slate-400 hover:text-blue-400 focus:outline-none transition p-2 hover:bg-[#152642] rounded-lg lg:hidden">
<i class="ph ph-list text-2xl"></i>
</button>
<h1 class="text-lg font-bold text-gradient hidden sm:block">
{{ organization.name|default:"Smart Edu Center" }}
</h1>
<div class="flex items-center gap-2">
<button
class="relative p-2.5 text-slate-400 hover:text-amber-400 hover:bg-[#152642] rounded-xl transition group">
<i class="ph ph-bell text-xl"></i>
<span class="absolute top-2 right-2 w-2 h-2 bg-rose-500 rounded-full animate-pulse"></span>
</button>
<button class="p-2.5 text-slate-400 hover:text-blue-400 hover:bg-[#152642] rounded-xl transition">
<i class="ph ph-gear text-xl"></i>
</button>
</div>
</header>
<main class="flex-1 overflow-y-auto bg-[#0a1628] p-6">
{% if messages %}
<div class="mb-6 space-y-3">
{% for message in messages %}
<div class="p-4 rounded-xl flex items-center gap-3 animate-fadeIn
{% if message.tags == 'error' %}bg-rose-500/10 text-rose-400 border border-rose-500/30
{% else %}bg-emerald-500/10 text-emerald-400 border border-emerald-500/30{% endif %}">
<i
class="ph {% if message.tags == 'error' %}ph-warning-circle{% else %}ph-check-circle{% endif %} text-xl"></i>
{{ message }}
</div>
{% endfor %}
</div>
{% endif %}
{% block content %}{% endblock %}
</main>
</div>
<div x-show="sidebarOpen && window.innerWidth < 1024" @click="sidebarOpen = false" x-transition.opacity
class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden" x-cloak></div>
</div>
</body>
</html>

--- templates\dashboard.html ---
{% extends 'base.html' %}
{% block title %}Boshqaruv Paneli{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<h1 class="text-2xl font-bold text-gray-800">Xush kelibsiz, {{ request.user.first_name }}! 👋</h1>
<div class="text-sm text-gray-500">Bugun: {% now "d F Y" %}</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Jami O'quvchilar</p>
<p class="text-2xl font-bold text-gray-800 mt-1">1,245</p>
<span class="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full font-medium">+12% o'sish</span>
</div>
<div class="p-3 bg-blue-50 rounded-lg text-blue-600">
<i class="ph ph-student text-2xl"></i>
</div>
</div>
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Yangi Lidlar</p>
<p class="text-2xl font-bold text-gray-800 mt-1">86</p>
<span class="text-xs text-orange-600 bg-orange-50 px-2 py-1 rounded-full font-medium">Bu oy</span>
</div>
<div class="p-3 bg-orange-50 rounded-lg text-orange-600">
<i class="ph ph-funnel text-2xl"></i>
</div>
</div>
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Oylik Tushum</p>
<p class="text-2xl font-bold text-gray-800 mt-1">45.2 M</p>
<span class="text-xs text-gray-400">UZS</span>
</div>
<div class="p-3 bg-green-50 rounded-lg text-green-600">
<i class="ph ph-wallet text-2xl"></i>
</div>
</div>
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Qarzdorlik</p>
<p class="text-2xl font-bold text-red-600 mt-1">3.5 M</p>
<span class="text-xs text-red-600 bg-red-50 px-2 py-1 rounded-full font-medium">Talab qilinadi</span>
</div>
<div class="p-3 bg-red-50 rounded-lg text-red-600">
<i class="ph ph-warning-circle text-2xl"></i>
</div>
</div>
</div>
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<div class="flex items-center justify-between mb-4">
<h3 class="font-bold text-gray-800">Bugungi Darslar</h3>
<a href="#" class="text-sm text-primary hover:underline">To'liq ko'rish</a>
</div>
<div class="space-y-4">
<div class="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-100">
<div class="w-16 text-center">
<span class="block text-sm font-bold text-gray-800">14:00</span>
<span class="block text-xs text-gray-500">15:30</span>
</div>
<div class="w-1 h-10 bg-blue-500 rounded-full mx-4"></div>
<div>
<h4 class="font-bold text-gray-800">General English (Beginner)</h4>
<p class="text-sm text-gray-500">Xona: 3-xona • O'qituvchi: Aziza Rahimova</p>
</div>
<div class="ml-auto">
<span class="px-3 py-1 text-xs font-bold text-blue-700 bg-blue-100 rounded-full">Darsda</span>
</div>
</div>
<div class="flex items-center p-3 bg-white rounded-lg border border-gray-100 hover:bg-gray-50">
<div class="w-16 text-center">
<span class="block text-sm font-bold text-gray-800">16:00</span>
<span class="block text-xs text-gray-500">17:30</span>
</div>
<div class="w-1 h-10 bg-green-500 rounded-full mx-4"></div>
<div>
<h4 class="font-bold text-gray-800">IELTS Foundation</h4>
<p class="text-sm text-gray-500">Xona: 5-xona • O'qituvchi: Bobur Aliyev</p>
</div>
<div class="ml-auto">
<span class="px-3 py-1 text-xs font-bold text-gray-600 bg-gray-100 rounded-full">Kutilmoqda</span>
</div>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<h3 class="font-bold text-gray-800 mb-4">So'nggi Lidlar</h3>
<div class="space-y-4">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center font-bold">
S
</div>
<div>
<h4 class="text-sm font-bold text-gray-800">Sardor Komilov</h4>
<p class="text-xs text-gray-500">+998 90 123 45 67</p>
</div>
<div class="ml-auto text-xs text-gray-400">15 daq</div>
</div>
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
M
</div>
<div>
<h4 class="text-sm font-bold text-gray-800">Madina Karimova</h4>
<p class="text-xs text-gray-500">Instagram</p>
</div>
<div class="ml-auto text-xs text-gray-400">1 soat</div>
</div>
</div>
<button class="w-full mt-6 py-2 text-sm text-center text-primary border border-primary rounded-lg hover:bg-primary hover:text-white transition-colors">
Barchasini ko'rish
</button>
</div>
</div>
</div>
{% endblock %}

--- templates\automation\template_form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto space-y-6">
<div class="flex items-center gap-4 mb-8">
<a href="{% url 'automation:template_list' %}"
class="p-3 bg-white hover:bg-gray-100 rounded-xl shadow-sm transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
</div>
<form method="POST" class="glass-panel p-8 rounded-2xl shadow-lg space-y-6">
{% csrf_token %}
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="space-y-2">
<label class="text-sm font-semibold text-gray-700">Nomi</label>
{{ form.title }}
</div>
<div class="space-y-2">
<label class="text-sm font-semibold text-gray-700">Kod (System Code)</label>
{{ form.code }}
<p class="text-xs text-gray-400">Tizim ichida chaqirish uchun</p>
</div>
</div>
<div class="space-y-2">
<label class="text-sm font-semibold text-gray-700">Xabar Turi</label>
{{ form.message_type }}
</div>
<div class="space-y-2">
<label class="text-sm font-semibold text-gray-700">Xabar Matni</label>
{{ form.body }}
<p class="text-xs text-gray-500 mt-1">
Mavjud o'zgaruvchilar: <code class="bg-gray-100 px-1 rounded">{first_name}</code>, <code
class="bg-gray-100 px-1 rounded">{last_name}</code>, <code
class="bg-gray-100 px-1 rounded">{phone}</code>
</p>
</div>
<div class="pt-6 border-t border-gray-100 flex justify-end gap-3">
<a href="{% url 'automation:template_list' %}"
class="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl transition">
Bekor qilish
</a>
<button type="submit"
class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl shadow-lg shadow-primary-500/30 transition flex items-center gap-2">
<i class="ph ph-check-circle text-xl"></i>
<span>Saqlash</span>
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\automation\template_list.html ---
{% extends 'base.html' %}
{% block title %}Xabar Shablonlari{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
Xabar Shablonlari
</h1>
<p class="text-gray-500">Avtomatik xabarlar matnini boshqarish</p>
</div>
<a href="{% url 'automation:template_create' %}"
class="px-5 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl shadow-lg shadow-primary-500/30 transition flex items-center gap-2">
<i class="ph ph-plus-circle text-xl"></i>
<span>Yangi Shablon</span>
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{% for template in templates %}
<div class="glass-panel p-6 rounded-2xl hover:shadow-xl transition-all duration-300 group">
<div class="flex justify-between items-start mb-4">
<div class="p-3 rounded-xl
{% if template.message_type == 'sms' %}bg-green-100 text-green-600
{% elif template.message_type == 'telegram' %}bg-blue-100 text-blue-600
{% else %}bg-gray-100 text-gray-600{% endif %}">
{% if template.message_type == 'sms' %}<i class="ph ph-chat-text text-2xl"></i>
{% elif template.message_type == 'telegram' %}<i class="ph ph-telegram-logo text-2xl"></i>
{% else %}<i class="ph ph-bell text-2xl"></i>{% endif %}
</div>
<div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
<a href="{% url 'automation:template_edit' template.pk %}"
class="p-2 hover:bg-gray-100 rounded-lg text-gray-600">
<i class="ph ph-pencil-simple"></i>
</a>
<form method="POST" action="{% url 'automation:template_delete' template.pk %}"
onsubmit="return confirm('O\'chirasizmi?')">
{% csrf_token %}
<button class="p-2 hover:bg-red-50 rounded-lg text-red-500">
<i class="ph ph-trash"></i>
</button>
</form>
</div>
</div>
<h3 class="text-lg font-bold text-gray-800 mb-1">{{ template.title }}</h3>
<code class="text-xs bg-gray-100 px-2 py-1 rounded text-gray-500 font-mono">{{ template.code }}</code>
<div class="mt-4 p-3 bg-gray-50 rounded-xl text-sm text-gray-600 line-clamp-3">
{{ template.body }}
</div>
</div>
{% empty %}
<div class="col-span-3 glass-panel p-12 text-center rounded-2xl">
<i class="ph ph-envelope-open text-6xl text-gray-300 mb-4 inline-block"></i>
<h3 class="text-xl font-bold text-gray-800">Shablonlar yo'q</h3>
<p class="text-gray-500 mt-2">Yangi shablon yaratish uchun yuqoridagi tugmani bosing</p>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\components\navbar.html ---
<header class="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-200 shadow-sm sticky top-0 z-20">
<button @click="sidebarOpen = !sidebarOpen" class="text-gray-500 focus:outline-none lg:hidden">
<i class="ph ph-list text-2xl"></i>
</button>
<div class="hidden md:flex items-center gap-2">
<i class="ph ph-buildings text-gray-400 text-lg"></i>
<span class="font-medium text-gray-600">{{ request.user.branch.name|default:"Bosh Filial" }}</span>
</div>
<div class="flex items-center gap-4">
<button class="relative p-2 text-gray-400 hover:text-primary transition-colors">
<i class="ph ph-bell text-xl"></i>
<span class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
</button>
<div class="relative" x-data="{ open: false }">
<button @click="open = !open" @click.outside="open = false" class="flex items-center gap-2 text-gray-600 hover:text-gray-900">
<i class="ph ph-gear text-xl"></i>
</button>
<div x-show="open" x-transition class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 border border-gray-100 z-50" x-cloak>
<a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Profil sozlamalari</a>
{% if request.user.role == 'super_admin' %}
<a href="/admin/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Admin Panel</a>
{% endif %}
<div class="border-t border-gray-100 my-1"></div>
<a href="{% url 'logout' %}" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50">Chiqish</a>
</div>
</div>
</div>
</header>

--- templates\components\search_results.html ---
<div class="divide-y divide-gray-100 dark:divide-dark-700">
{% if results %}
{% for result in results %}
<a href="{{ result.url }}"
class="flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-dark-700 transition group">
<div class="w-10 h-10 rounded-xl
{% if result.type == 'user' %}bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600
{% elif result.type == 'lead' %}bg-green-100 dark:bg-green-900/30 text-green-600
{% else %}bg-purple-100 dark:bg-purple-900/30 text-purple-600{% endif %}
flex items-center justify-center">
<i class="ph {{ result.icon }} text-xl"></i>
</div>
<div class="flex-1 min-w-0">
<p class="font-medium text-gray-800 dark:text-white truncate group-hover:text-indigo-600">
{{ result.title }}
</p>
<p class="text-xs text-gray-500 truncate">{{ result.subtitle }}</p>
</div>
<i class="ph ph-arrow-right text-gray-400 group-hover:text-indigo-500 transition"></i>
</a>
{% endfor %}
{% else %}
<div class="p-6 text-center text-gray-500">
<i class="ph ph-magnifying-glass text-3xl mb-2"></i>
<p>"{{ query }}" bo'yicha hech narsa topilmadi</p>
</div>
{% endif %}
</div>

--- templates\components\sidebar.html ---
<a href="{% url 'dashboard' %}"
class="sidebar-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
<i class="ph-fill ph-squares-four"></i>
<span>Dashboard</span>
</a>
{% if request.user.role in 'super_admin,owner,admin' %}
<p class="sidebar-section">Boshqaruv</p>
<a href="{% url 'user_list' %}" class="sidebar-link {% if 'users' in request.path %}active{% endif %}">
<i class="ph-fill ph-users"></i>
<span>Foydalanuvchilar</span>
</a>
<a href="{% url 'automation:template_list' %}"
class="sidebar-link {% if 'automation' in request.path %}active{% endif %}">
<i class="ph-fill ph-robot"></i>
<span>Avtomatizatsiya</span>
</a>
{% endif %}
{% if request.user.role in 'super_admin,owner,admin,manager' %}
<p class="sidebar-section">Sotuv & CRM</p>
<a href="{% url 'pipeline' %}" class="sidebar-link {% if 'pipeline' in request.path %}active{% endif %}">
<i class="ph-fill ph-kanban"></i>
<span>Voronka</span>
</a>
<a href="{% url 'stage_list' %}" class="sidebar-link {% if 'stages' in request.path %}active{% endif %}">
<i class="ph-fill ph-rows"></i>
<span>Bosqichlar</span>
</a>
<a href="{% url 'source_list' %}" class="sidebar-link {% if 'sources' in request.path %}active{% endif %}">
<i class="ph-fill ph-megaphone"></i>
<span>Manbalar</span>
</a>
{% endif %}
{% if request.user.role in 'super_admin,owner,admin,teacher' %}
<p class="sidebar-section">O'quv Jarayoni</p>
<a href="{% url 'group_list' %}" class="sidebar-link {% if 'groups' in request.path %}active{% endif %}">
<i class="ph-fill ph-users-three"></i>
<span>Guruhlar</span>
</a>
<a href="{% url 'course_list' %}" class="sidebar-link {% if 'courses' in request.path %}active{% endif %}">
<i class="ph-fill ph-books"></i>
<span>Kurslar</span>
</a>
<a href="{% url 'room_list' %}" class="sidebar-link {% if 'rooms' in request.path %}active{% endif %}">
<i class="ph-fill ph-door"></i>
<span>Xonalar</span>
</a>
<a href="{% url 'material_list' %}" class="sidebar-link {% if 'materials' in request.path %}active{% endif %}">
<i class="ph-fill ph-file-video"></i>
<span>Materiallar</span>
</a>
{% endif %}
{% if request.user.role in 'super_admin,owner,admin,teacher' %}
<p class="sidebar-section">Operatsiyalar</p>
<a href="{% url 'operations:lesson_list' %}" class="sidebar-link {% if 'lessons' in request.path %}active{% endif %}">
<i class="ph-fill ph-chalkboard"></i>
<span>Darslar</span>
</a>
<a href="{% url 'operations:schedule' %}" class="sidebar-link {% if 'schedule' in request.path %}active{% endif %}">
<i class="ph-fill ph-calendar"></i>
<span>Jadval</span>
</a>
{% endif %}
<p class="sidebar-section">Reytinglar</p>
<a href="{% url 'operations:teacher_ratings' %}"
class="sidebar-link {% if 'ratings/teachers' in request.path %}active{% endif %}">
<i class="ph-fill ph-trophy"></i>
<span>O'qituvchilar</span>
</a>
<a href="{% url 'operations:student_ratings' %}"
class="sidebar-link {% if 'ratings/students' in request.path %}active{% endif %}">
<i class="ph-fill ph-medal"></i>
<span>O'quvchilar</span>
</a>
<a href="{% url 'operations:shop' %}" class="sidebar-link {% if 'shop' in request.path %}active{% endif %}">
<i class="ph-fill ph-storefront"></i>
<span>Do'kon</span>
</a>
{% if request.user.role in 'super_admin,owner,admin' %}
<p class="sidebar-section">Moliya</p>
<a href="{% url 'finance:account_list' %}" class="sidebar-link {% if 'accounts' in request.path %}active{% endif %}">
<i class="ph-fill ph-vault"></i>
<span>Kassalar</span>
</a>
<a href="{% url 'finance:transaction_list' %}"
class="sidebar-link {% if 'transactions' in request.path %}active{% endif %}">
<i class="ph-fill ph-arrows-left-right"></i>
<span>Kirim-Chiqim</span>
</a>
<a href="{% url 'finance:report' %}" class="sidebar-link {% if 'report' in request.path %}active{% endif %}">
<i class="ph-fill ph-chart-bar"></i>
<span>Hisobotlar</span>
</a>
<a href="{% url 'finance:payroll_list' %}" class="sidebar-link {% if 'payroll' in request.path %}active{% endif %}">
<i class="ph-fill ph-money"></i>
<span>Oyliklar</span>
</a>
<a href="{% url 'finance:staff_attendance_list' %}" class="sidebar-link {% if 'hr' in request.path %}active{% endif %}">
<i class="ph-fill ph-fingerprint"></i>
<span>HR Davomat</span>
</a>
<a href="{% url 'finance:supply_list' %}" class="sidebar-link {% if 'supplies' in request.path %}active{% endif %}">
<i class="ph-fill ph-package"></i>
<span>Sklad</span>
</a>
<a href="{% url 'finance:pending_receipts' %}"
class="sidebar-link {% if 'receipts' in request.path %}active{% endif %}">
<i class="ph-fill ph-receipt"></i>
<span>Chek Tekshirish</span>
</a>
<a href="{% url 'core:history_list' %}" class="sidebar-link {% if 'history' in request.path %}active{% endif %}">
<i class="ph-fill ph-clock-counter-clockwise"></i>
<span>Tarix</span>
</a>
{% endif %}

--- templates\core\history.html ---
{% extends 'base.html' %}
{% block title %}Tizim Tarixi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
<i class="ph ph-clock-counter-clockwise text-primary-500"></i>
Tizim Tarixi
</h1>
<p class="text-gray-500 dark:text-gray-400">Barcha amallar va o'zgarishlar logi</p>
</div>
</div>
<div class="glass-panel rounded-2xl border border-gray-100 dark:border-gray-800 p-6">
<form method="GET" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
<div class="lg:col-span-2">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Qidirish</label>
<div class="relative">
<input type="text" name="q" value="{{ current_search|default:'' }}"
placeholder="Ism, model, obyekt..." class="w-full pl-10">
<i class="ph ph-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Amal</label>
<select name="action" class="w-full">
<option value="">Barchasi</option>
{% for value, label in action_choices %}
<option value="{{ value }}" {% if current_action == value %}selected{% endif %}>{{ label }}</option>
{% endfor %}
</select>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Foydalanuvchi</label>
<select name="user" class="w-full">
<option value="">Barchasi</option>
{% for user in users %}
<option value="{{ user.id }}" {% if current_user == user.id|stringformat:"s" %}selected{% endif %}>
{{ user.first_name }} {{ user.last_name }}
</option>
{% endfor %}
</select>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sanadan</label>
<input type="date" name="date_from" value="{{ date_from|default:'' }}" class="w-full">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sanagacha</label>
<input type="date" name="date_to" value="{{ date_to|default:'' }}" class="w-full">
</div>
<div class="lg:col-span-6 flex items-center gap-3">
<button type="submit"
class="px-6 py-2.5 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 transition flex items-center gap-2">
<i class="ph ph-funnel"></i> Filtrlash
</button>
<a href="{% url 'core:history_list' %}"
class="px-4 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-xl font-medium hover:bg-gray-200 dark:hover:bg-gray-700 transition">
Tozalash
</a>
</div>
</form>
</div>
<div class="glass-panel rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
<div class="overflow-x-auto">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-gray-800/50">
<tr>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Vaqt</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Foydalanuvchi</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Amal</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Bo'lim</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Obyekt</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">IP
</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
{% for log in logs %}
<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
<td class="px-6 py-4 whitespace-nowrap">
<div class="text-sm font-medium text-gray-900 dark:text-white">{{
log.created_at|date:"d.m.Y" }}</div>
<div class="text-xs text-gray-500">{{ log.created_at|time:"H:i:s" }}</div>
</td>
<td class="px-6 py-4 whitespace-nowrap">
<div class="flex items-center gap-3">
<div
class="w-8 h-8 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
{{ log.user.first_name|first|default:"?" }}
</div>
<div>
<div class="text-sm font-medium text-gray-900 dark:text-white">
{{ log.user.first_name|default:"Tizim" }} {{ log.user.last_name|default:"" }}
</div>
<div class="text-xs text-gray-500">{{ log.user.role|default:"-" }}</div>
</div>
</div>
</td>
<td class="px-6 py-4 whitespace-nowrap">
<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium
{% if log.action == 'CREATE' %}bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400
{% elif log.action == 'UPDATE' %}bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400
{% elif log.action == 'DELETE' %}bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400
{% elif log.action == 'LOGIN' %}bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-400
{% else %}bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400{% endif %}">
{% if log.action == 'CREATE' %}<i class="ph ph-plus-circle"></i>
{% elif log.action == 'UPDATE' %}<i class="ph ph-pencil"></i>
{% elif log.action == 'DELETE' %}<i class="ph ph-trash"></i>
{% elif log.action == 'LOGIN' %}<i class="ph ph-sign-in"></i>
{% else %}<i class="ph ph-sign-out"></i>{% endif %}
{{ log.get_action_display }}
</span>
</td>
<td class="px-6 py-4 whitespace-nowrap">
<span
class="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs text-gray-600 dark:text-gray-400">
{{ log.model_name }}
</span>
</td>
<td class="px-6 py-4">
<div class="text-sm text-gray-900 dark:text-white max-w-xs truncate"
title="{{ log.object_repr }}">
{{ log.object_repr|default:"-" }}
</div>
{% if log.object_id %}
<div class="text-xs text-gray-500">ID: {{ log.object_id }}</div>
{% endif %}
</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
{{ log.ip_address|default:"-" }}
</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="px-6 py-12 text-center">
<div class="flex flex-col items-center">
<div
class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
<i class="ph ph-clock text-3xl text-gray-400"></i>
</div>
<p class="text-gray-500 dark:text-gray-400">Hozircha tarix yo'q</p>
</div>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
{% if logs.has_other_pages %}
<div class="px-6 py-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
<div class="text-sm text-gray-500">
{{ logs.start_index }} - {{ logs.end_index }} / {{ logs.paginator.count }} ta
</div>
<div class="flex items-center gap-2">
{% if logs.has_previous %}
<a href="?page={{ logs.previous_page_number }}{% if current_action %}&action={{ current_action }}{% endif %}{% if current_user %}&user={{ current_user }}{% endif %}{% if current_search %}&q={{ current_search }}{% endif %}"
class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-caret-left"></i>
</a>
{% endif %}
<span
class="px-3 py-1.5 bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-400 rounded-lg text-sm font-medium">
{{ logs.number }}
</span>
{% if logs.has_next %}
<a href="?page={{ logs.next_page_number }}{% if current_action %}&action={{ current_action }}{% endif %}{% if current_user %}&user={{ current_user }}{% endif %}{% if current_search %}&q={{ current_search }}{% endif %}"
class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-caret-right"></i>
</a>
{% endif %}
</div>
</div>
{% endif %}
</div>
</div>
{% endblock %}

--- templates\crm\lead_convert.html ---
{% extends 'base.html' %}
{% block title %}O'quvchiga aylantirish{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="{% url 'lead_detail' lead.pk %}" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800">O'quvchiga aylantirish</h1>
<p class="text-gray-500">{{ lead.full_name }} → Yangi O'quvchi</p>
</div>
</div>
<form method="POST" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
{% csrf_token %}
<div>
<h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
<i class="ph ph-student text-primary"></i> O'quvchi ma'lumotlari
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Ism *</label>
{{ form.first_name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Familiya *</label>
{{ form.last_name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Telefon *</label>
{{ form.phone }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Parol</label>
{{ form.password }}
<p class="text-xs text-gray-400 mt-1">Bo'sh qoldirsangiz avtomatik yaratiladi</p>
</div>
</div>
</div>
<hr class="border-gray-200">
<div>
<h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
<i class="ph ph-users text-green-600"></i> Ota-ona ma'lumotlari
<span class="text-xs text-red-500 font-normal">(Majburiy)</span>
</h3>
<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
<p class="text-sm text-yellow-700">
<i class="ph ph-warning"></i> O'quvchi qo'shish uchun ota-ona ma'lumotlari majburiy!
</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Ota-ona ismi *</label>
{{ form.parent_first_name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Ota-ona familiyasi</label>
{{ form.parent_last_name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Telefon raqami *</label>
{{ form.parent_phone }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Qarindoshligi *</label>
{{ form.relation_type }}
</div>
</div>
</div>
<div class="flex justify-end gap-4 pt-4 border-t">
<a href="{% url 'lead_detail' lead.pk %}"
class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
Bekor qilish
</a>
<button type="submit"
class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition flex items-center gap-2">
<i class="ph ph-check-circle"></i> O'quvchi yaratish
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\crm\lead_detail.html ---
{% extends 'base.html' %}
{% block title %}{{ lead.full_name }}{% endblock %}
{% block content %}
<div class="space-y-8 max-w-7xl mx-auto">
<div
class="relative bg-white dark:bg-dark-800 rounded-3xl p-8 shadow-xl shadow-gray-100/50 dark:shadow-none border border-gray-100 dark:border-gray-700 overflow-hidden">
<div
class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 rounded-full blur-3xl opacity-60 -mr-16 -mt-16 pointer-events-none">
</div>
<div class="relative flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
<div class="flex items-center gap-6">
<a href="{% url 'pipeline' %}"
class="group p-3 bg-white dark:bg-dark-700 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-600 hover:shadow-md hover:scale-105 transition-all duration-300">
<i
class="ph ph-arrow-left text-xl text-gray-500 group-hover:text-primary-600 dark:text-gray-400"></i>
</a>
<div>
<h1
class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300">
{{ lead.full_name }}</h1>
<div class="flex items-center gap-2 mt-2 text-gray-500 dark:text-gray-400">
<span
class="inline-flex items-center gap-1.5 px-3 py-1 bg-gray-50 dark:bg-gray-700/50 rounded-lg text-sm font-medium">
<i class="ph-fill ph-phone text-primary-500"></i> {{ lead.phone }}
</span>
<span
class="inline-flex items-center gap-1.5 px-3 py-1 bg-gray-50 dark:bg-gray-700/50 rounded-lg text-sm font-medium">
<i class="ph-fill ph-calendar text-gray-400"></i> {{ lead.created_at|date:"d M Y" }}
</span>
</div>
</div>
</div>
<div class="flex items-center gap-3 w-full md:w-auto">
<a href="{% url 'lead_edit' lead.pk %}"
class="flex-1 md:flex-none justify-center px-6 py-3 bg-white dark:bg-dark-700 text-gray-700 dark:text-gray-200 font-medium rounded-2xl border border-gray-200 dark:border-gray-600 shadow-sm hover:shadow-md hover:bg-gray-50 dark:hover:bg-dark-600 transition-all duration-300 flex items-center gap-2">
<i class="ph ph-pencil-simple text-lg"></i> Tahrirlash
</a>
<a href="{% url 'lead_convert' lead.pk %}"
class="flex-1 md:flex-none justify-center px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-2xl shadow-lg shadow-green-500/20 hover:shadow-xl hover:shadow-green-500/30 hover:-translate-y-0.5 transition-all duration-300 flex items-center gap-2">
<i class="ph-bold ph-student text-lg"></i> O'quvchiga o'tkazish
</a>
</div>
</div>
</div>
<div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
<div class="lg:col-span-4 space-y-8">
<div
class="bg-white dark:bg-dark-800 rounded-3xl p-6 shadow-xl shadow-gray-100/50 dark:shadow-none border border-gray-100 dark:border-gray-700">
<h3 class="font-bold text-gray-800 dark:text-gray-100 mb-6 flex items-center gap-2">
<i class="ph-fill ph-flag text-primary-500 text-xl"></i> Hozirgi holat
</h3>
<div class="relative overflow-hidden rounded-2xl p-6 mb-8 transition-all duration-300"
style="background: linear-gradient(135deg, {{ lead.stage.color }}15 0%, {{ lead.stage.color }}05 100%); border: 1px solid {{ lead.stage.color }}30;">
<div class="flex items-center gap-4">
<div class="w-12 h-12 rounded-xl flex items-center justify-center shadow-sm"
style="background-color: {{ lead.stage.color }}; color: white;">
<i class="ph-bold ph-hash text-2xl"></i>
</div>
<div>
<p class="text-sm opacity-70" style="color: {{ lead.stage.color }}">Bosqich</p>
<p class="font-bold text-lg" style="color: {{ lead.stage.color }}">{{ lead.stage.name }}</p>
</div>
</div>
</div>
<div class="space-y-3">
<p class="text-xs font-semibold text-gray-400 uppercase tracking-wider pl-1">Bosqichni o'zgartirish
</p>
<div class="grid grid-cols-2 gap-2">
{% for stage in stages %}
{% if stage.id != lead.stage.id %}
<form method="POST" action="{% url 'update_lead_stage' lead.id %}" class="w-full">
{% csrf_token %}
<button type="button" onclick="updateStage({{ lead.id }}, {{ stage.id }})"
class="w-full text-left px-4 py-3 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-500 hover:bg-gray-50 dark:hover:bg-dark-700 transition-all duration-200 group flex items-center gap-2 relative overflow-hidden">
<span
class="w-2 h-8 rounded-full absolute left-0 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity"
style="background-color: {{ stage.color }}"></span>
<span class="w-3 h-3 rounded-full" style="background-color: {{ stage.color }}"></span>
<span
class="text-sm font-medium text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white truncate">{{
stage.name }}</span>
</button>
</form>
{% endif %}
{% endfor %}
</div>
</div>
</div>
<div
class="bg-white dark:bg-dark-800 rounded-3xl p-6 shadow-xl shadow-gray-100/50 dark:shadow-none border border-gray-100 dark:border-gray-700">
<h3 class="font-bold text-gray-800 dark:text-gray-100 mb-6 flex items-center gap-2">
<i class="ph-fill ph-info text-blue-500 text-xl"></i> Ma'lumotlar
</h3>
<div class="space-y-5">
<div
class="group flex items-center gap-4 p-3 hover:bg-gray-50 dark:hover:bg-dark-700/50 rounded-2xl transition-colors">
<div
class="w-12 h-12 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform duration-300">
<i class="ph-fill ph-phone text-xl"></i>
</div>
<div>
<p class="text-xs text-gray-400 font-medium">Telefon raqam</p>
<p class="font-semibold text-gray-800 dark:text-gray-200">{{ lead.phone }}</p>
</div>
</div>
<div
class="group flex items-center gap-4 p-3 hover:bg-gray-50 dark:hover:bg-dark-700/50 rounded-2xl transition-colors">
<div
class="w-12 h-12 bg-purple-50 dark:bg-purple-900/20 rounded-2xl flex items-center justify-center text-purple-600 dark:text-purple-400 group-hover:scale-110 transition-transform duration-300">
<i class="ph-fill ph-broadcast text-xl"></i>
</div>
<div>
<p class="text-xs text-gray-400 font-medium">Manba</p>
<p class="font-semibold text-gray-800 dark:text-gray-200">{{
lead.source.name|default:"Noma'lum" }}</p>
</div>
</div>
{% if lead.interested_course %}
<div
class="group flex items-center gap-4 p-3 hover:bg-gray-50 dark:hover:bg-dark-700/50 rounded-2xl transition-colors">
<div
class="w-12 h-12 bg-green-50 dark:bg-green-900/20 rounded-2xl flex items-center justify-center text-green-600 dark:text-green-400 group-hover:scale-110 transition-transform duration-300">
<i class="ph-fill ph-graduation-cap text-xl"></i>
</div>
<div>
<p class="text-xs text-gray-400 font-medium">Qiziqqan kursi</p>
<p class="font-semibold text-gray-800 dark:text-gray-200">{{ lead.interested_course.name }}
</p>
</div>
</div>
{% endif %}
<div
class="group flex items-center gap-4 p-3 hover:bg-gray-50 dark:hover:bg-dark-700/50 rounded-2xl transition-colors">
<div
class="w-12 h-12 bg-orange-50 dark:bg-orange-900/20 rounded-2xl flex items-center justify-center text-orange-600 dark:text-orange-400 group-hover:scale-110 transition-transform duration-300">
<i class="ph-fill ph-user-circle text-xl"></i>
</div>
<div>
<p class="text-xs text-gray-400 font-medium">Mas'ul xodim</p>
<p class="font-semibold text-gray-800 dark:text-gray-200">{{
lead.assigned_to.first_name|default:"Biriktirilmagan" }}</p>
</div>
</div>
</div>
</div>
{% if lead.extra_data %}
<div
class="bg-white dark:bg-dark-800 rounded-3xl p-6 shadow-xl shadow-gray-100/50 dark:shadow-none border border-gray-100 dark:border-gray-700">
<h3 class="font-bold text-gray-800 dark:text-gray-100 mb-4">Qo'shimcha ma'lumotlar</h3>
<div class="bg-gray-50 dark:bg-dark-900 p-4 rounded-2xl border border-gray-100 dark:border-gray-700">
<pre
class="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap font-mono">{{ lead.extra_data|pprint }}</pre>
</div>
</div>
{% endif %}
</div>
<div class="lg:col-span-8">
<div
class="bg-white dark:bg-dark-800 rounded-3xl p-6 md:p-8 shadow-xl shadow-gray-100/50 dark:shadow-none border border-gray-100 dark:border-gray-700 h-full">
<div class="flex items-center justify-between mb-8">
<h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-3">
<span
class="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
<i class="ph-bold ph-clock-counter-clockwise"></i>
</span>
Faoliyat tarixi
</h3>
</div>
<form method="POST" action="{% url 'add_lead_activity' lead.pk %}"
class="mb-10 bg-gray-50 dark:bg-dark-700/30 p-2 rounded-[24px] border border-gray-100 dark:border-gray-700 focus-within:ring-4 focus-within:ring-primary-100 dark:focus-within:ring-primary-900/30 transition-all duration-300">
{% csrf_token %}
<div class="flex flex-col sm:flex-row gap-2">
<div class="relative min-w-[140px]">
<select name="activity_type"
class="w-full appearance-none bg-white dark:bg-dark-800 pl-10 pr-8 py-3.5 rounded-2xl border-0 text-sm font-semibold text-gray-700 dark:text-gray-200 cursor-pointer hover:bg-gray-50 dark:hover:bg-dark-700 focus:ring-0 transition-colors">
<option value="call">📞 Qo'ng'iroq</option>
<option value="sms">💬 SMS</option>
<option value="meeting">🤝 Uchrashuv</option>
<option value="note" selected>📝 Izoh</option>
</select>
<i
class="ph-bold ph-caret-down absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
<div
class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none flex items-center justify-center">
</div>
</div>
<div class="flex-1 flex gap-2">
<input type="text" name="comment" placeholder="Yangi faoliyat yoki izoh qoldiring..."
required
class="flex-1 bg-transparent border-0 py-3.5 px-4 text-gray-800 dark:text-gray-100 placeholder-gray-400 focus:ring-0">
<button type="submit"
class="p-3.5 bg-primary-600 hover:bg-primary-700 text-white rounded-2xl transition-colors shadow-lg shadow-primary-600/20">
<i class="ph-bold ph-paper-plane-right text-lg"></i>
</button>
</div>
</div>
</form>
<div
class="relative pl-4 sm:pl-8 space-y-8 before:content-[''] before:absolute before:left-4 sm:before:left-8 before:top-4 before:bottom-4 before:w-[2px] before:bg-gray-100 dark:before:bg-dark-700">
{% for activity in activities %}
<div class="relative pl-8 sm:pl-10 group">
<div class="absolute left-0 sm:left-4 top-1 -translate-x-1/2 w-8 h-8 rounded-full border-4 border-white dark:border-dark-800 flex items-center justify-center z-10
{% if activity.activity_type == 'call' %}bg-green-100 text-green-600 ring-2 ring-green-500/20
{% elif activity.activity_type == 'sms' %}bg-blue-100 text-blue-600 ring-2 ring-blue-500/20
{% elif activity.activity_type == 'meeting' %}bg-purple-100 text-purple-600 ring-2 ring-purple-500/20
{% elif activity.activity_type == 'status_change' %}bg-orange-100 text-orange-600 ring-2 ring-orange-500/20
{% else %}bg-gray-100 text-gray-600 ring-2 ring-gray-500/20{% endif %}">
{% if activity.activity_type == 'call' %}<i class="ph-fill ph-phone text-xs"></i>
{% elif activity.activity_type == 'sms' %}<i
class="ph-fill ph-chat-circle-text text-xs"></i>
{% elif activity.activity_type == 'meeting' %}<i class="ph-fill ph-users-three text-xs"></i>
{% elif activity.activity_type == 'status_change' %}<i
class="ph-bold ph-arrows-left-right text-xs"></i>
{% else %}<i class="ph-fill ph-note-pencil text-xs"></i>{% endif %}
</div>
<div
class="bg-gray-50 dark:bg-dark-700/30 p-5 rounded-2xl rounded-tl-none border border-transparent hover:border-gray-200 dark:hover:border-gray-600 transition-colors">
<div class="flex flex-wrap items-center justify-between gap-2 mb-2">
<span class="font-bold text-gray-900 dark:text-gray-100 text-sm">{{
activity.user.first_name|default:"Tizim" }}</span>
<span
class="text-xs font-medium text-gray-400 bg-white dark:bg-dark-800 px-2 py-1 rounded-md border border-gray-100 dark:border-gray-700">
{{ activity.created_at|timesince }} oldin
</span>
</div>
<p class="text-gray-600 dark:text-gray-300 leading-relaxed text-sm">{{ activity.comment }}
</p>
</div>
</div>
{% empty %}
<div class="text-center py-12">
<div
class="w-16 h-16 bg-gray-50 dark:bg-dark-700 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300 dark:text-gray-600">
<i class="ph-duotone ph-chats-teardrop text-3xl"></i>
</div>
<p class="text-gray-500 dark:text-gray-400 font-medium">Hozircha faoliyat tarixi mavjud emas</p>
<p class="text-sm text-gray-400 dark:text-gray-500">Birinchi izoh yoki faoliyatni qo'shing</p>
</div>
{% endfor %}
</div>
</div>
</div>
</div>
</div>
<script>
function updateStage(leadId, stageId) {
fetch(`/crm/api/leads/${leadId}/move/`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'X-CSRFToken': '{{ csrf_token }}'
},
body: JSON.stringify({ stage_id: stageId })
})
.then(response => response.json())
.then(data => {
if (data.status === 'success') {
location.reload();
} else {
alert("Xatolik yuz berdi!");
}
})
.catch(error => {
console.error('Error:', error);
alert("Server bilan aloqa xatosi!");
});
}
</script>
{% endblock %}

--- templates\crm\lead_form.html ---
{% extends 'base.html' %}
{% block content %}
<div class="max-w-lg mx-auto bg-white p-6 rounded-xl shadow-sm border border-gray-100">
<h2 class="text-xl font-bold mb-6">Yangi Lid Qo'shish</h2>
{% if form.errors %}
<div class="bg-red-50 text-red-600 p-4 rounded-lg mb-4 text-sm">
{{ form.non_field_errors }}
{% for field in form %}
{% if field.errors %}
<p><b>{{ field.label }}:</b> {{ field.errors|striptags }}</p>
{% endif %}
{% endfor %}
</div>
{% endif %}
<form method="post" class="space-y-4">
{% csrf_token %}
<div><label class="font-medium text-sm">Ism Familiya</label>{{ form.full_name }}</div>
<div><label class="font-medium text-sm">Telefon</label>{{ form.phone }}</div>
<div class="grid grid-cols-2 gap-4">
<div><label class="font-medium text-sm">Manba</label>{{ form.source }}</div>
<div><label class="font-medium text-sm">Kurs</label>{{ form.interested_course }}</div>
</div>
<div><label class="font-medium text-sm">Izoh</label>{{ form.extra_data }}</div>
<button type="submit" class="w-full bg-primary text-white py-3 rounded-lg font-bold hover:bg-indigo-700 transition">
Saqlash
</button>
</form>
</div>
{% endblock %}

--- templates\crm\pipeline.html ---
{% extends 'base.html' %}
{% load static %}
{% block title %}Sotuv Voronkasi{% endblock %}
{% block content %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js"></script>
<div class="h-[calc(100vh-8rem)] flex flex-col">
<div class="flex justify-between items-center mb-6">
<h1 class="text-2xl font-bold text-gray-800">Sotuv Voronkasi</h1>
<a href="{% url 'lead_create' %}"
class="bg-primary hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition shadow-sm">
<i class="ph ph-plus"></i> Yangi Lid
</a>
</div>
<div class="flex gap-6 overflow-x-auto pb-6 h-full items-start px-2">
{% for stage in stages %}
<div
class="flex-shrink-0 w-80 flex flex-col h-full bg-white/40 dark:bg-dark-800/40 backdrop-blur-md rounded-2xl border border-white/20 dark:border-white/5 shadow-glass">
<div
class="p-4 border-b border-white/20 dark:border-white/5 flex justify-between items-center bg-white/30 dark:bg-dark-800/30 rounded-t-2xl backdrop-blur-sm">
<div class="flex items-center gap-3">
<span class="w-2.5 h-10 rounded-full shadow-lg shadow-current"
style="background-color: {{ stage.color }};"></span>
<h3 class="font-bold text-gray-800 dark:text-white">{{ stage.name }}</h3>
</div>
<span
class="bg-white/50 dark:bg-white/10 text-gray-600 dark:text-gray-300 text-xs px-2.5 py-1 rounded-lg font-bold border border-white/20 shadow-sm">
{{ stage.leads.count }}
</span>
</div>
<div class="p-4 flex-1 overflow-y-auto space-y-3 sortable-list custom-scrollbar"
data-stage-id="{{ stage.id }}">
{% for lead in stage.leads.all %}
<div class="bg-white/80 dark:bg-dark-700/80 p-4 rounded-xl shadow-lg border border-white/40 dark:border-white/5 hover:scale-[1.02] hover:shadow-xl hover:border-blue-400/50 transition-all duration-300 cursor-grab active:cursor-grabbing group relative backdrop-blur-sm"
data-lead-id="{{ lead.id }}">
<div class="flex justify-between items-start mb-3">
<h4 class="font-bold text-gray-800 dark:text-gray-100 truncate pr-2 capitalize">{{ lead.full_name }}</h4>
<a href="{% url 'lead_detail' lead.id %}"
class="text-gray-400 hover:text-blue-500 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-blue-50 rounded">
<i class="ph ph-pencil-simple"></i>
</a>
</div>
<div class="space-y-2">
<div class="text-xs font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
<div class="p-1 rounded bg-indigo-50 dark:bg-indigo-900/30 text-indigo-500">
<i class="ph ph-phone"></i>
</div>
{{ lead.phone }}
</div>
{% if lead.interested_course %}
<div
class="text-xs text-indigo-600 dark:text-indigo-300 font-semibold bg-indigo-50 dark:bg-indigo-900/40 inline-block px-2.5 py-1 rounded-lg border border-indigo-100 dark:border-indigo-800/50">
{{ lead.interested_course.name }}
</div>
{% endif %}
</div>
<div
class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 flex justify-between items-center text-[10px] uppercase font-bold tracking-wider text-gray-400">
<span class="flex items-center gap-1">
<i class="ph ph-arrow-elbow-down-right"></i> {{ lead.source.name|default:"-" }}
</span>
<span class="bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded text-gray-500">{{ lead.created_at|date:"d M" }}</span>
</div>
</div>
{% endfor %}
</div>
</div>
{% empty %}
<div
class="flex items-center justify-center w-full h-64 text-gray-400 dark:text-gray-500 glass-panel rounded-2xl">
<div class="text-center">
<i class="ph ph-kanban text-4xl mb-3 opacity-50"></i>
<p>Hozircha bosqichlar yo'q</p>
<a href="#" class="text-primary hover:underline text-sm mt-2 block">Bosqich qo'shish +</a>
</div>
</div>
{% endfor %}
</div>
</div>
<script>
const lists = document.querySelectorAll('.sortable-list');
lists.forEach(list => {
new Sortable(list, {
group: 'shared', // Hamma ustunlar bir guruhda (biridan ikkinchisiga o'tadi)
animation: 150,
ghostClass: 'bg-blue-50', // Sudrayotganda orqada qolgan joy rangi
// DROP BO'LGANDA ISHLAYDI
onEnd: function (evt) {
const itemEl = evt.item;  // Surilgan karta
const newStageEl = evt.to; // Tushgan yangi ustun
const leadId = itemEl.getAttribute('data-lead-id');
const newStageId = newStageEl.getAttribute('data-stage-id');
// Agar joyi o'zgarmagan bo'lsa, to'xtaymiz
if (evt.from === evt.to) return;
// SERVERGA YUBORISH (AJAX)
fetch(`/crm/api/leads/${leadId}/move/`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'X-CSRFToken': '{{ csrf_token }}'
},
body: JSON.stringify({ stage_id: newStageId })
})
.then(response => response.json())
.then(data => {
if (data.status === 'success') {
console.log("Status o'zgardi!");
// Bu yerda Toast xabar chiqarish mumkin
} else {
alert("Xatolik yuz berdi!");
// Joyiga qaytarish (agar xato bo'lsa)
// location.reload();
}
});
}
});
});
</script>
{% endblock %}

--- templates\crm\source_list.html ---
{% extends 'base.html' %}
{% block title %}Manbalar{% endblock %}
{% block header_title %}📣 Lidlar Manbalari{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Manbalar</h1>
<a href="{% url 'source_create' %}"
class="px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition flex items-center gap-2">
<i class="ph ph-plus"></i> Yangi Manba
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{% for source in sources %}
<div class="glass-panel p-5 rounded-2xl hover:shadow-lg transition">
<div class="flex items-center justify-between">
<div class="flex items-center gap-3">
<div
class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white text-xl">
<i class="ph ph-megaphone"></i>
</div>
<div>
<h3 class="font-bold text-gray-800 dark:text-white">{{ source.name }}</h3>
<p class="text-sm text-gray-500">{{ source.lead_count }} lid</p>
</div>
</div>
<a href="{% url 'source_update' source.id %}"
class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 text-gray-500">
<i class="ph ph-pencil"></i>
</a>
</div>
</div>
{% empty %}
<div class="col-span-full text-center py-12 text-gray-500">
<i class="ph ph-megaphone text-5xl mb-4"></i>
<p>Hozircha manbalar yo'q</p>
<a href="{% url 'source_create' %}" class="text-indigo-600 hover:underline mt-2 inline-block">+ Yangi manba
qo'shish</a>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\crm\stage_form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="{% url 'stage_list' %}" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
</div>
<form method="POST" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
{% csrf_token %}
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Bosqich nomi *</label>
{{ form.name }}
</div>
<div class="grid grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Tartib raqami *</label>
{{ form.order }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Rang</label>
{{ form.color }}
</div>
</div>
<div class="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
{{ form.is_won }}
<div>
<label class="font-medium text-gray-700">Yutuq bosqichi</label>
<p class="text-xs text-gray-500">Agar lid bu bosqichga o'tsa, u o'quvchiga aylangani hisoblanadi</p>
</div>
</div>
<div class="flex justify-end gap-4 pt-4 border-t">
<a href="{% url 'stage_list' %}"
class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
Bekor qilish
</a>
<button type="submit" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 transition">
Saqlash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\crm\stage_list.html ---
{% extends 'base.html' %}
{% block title %}Voronka Bosqichlari{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Voronka Bosqichlari</h1>
<p class="text-gray-500">Sotuv voronkasi bosqichlarini boshqaring</p>
</div>
<a href="{% url 'stage_create' %}"
class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 shadow-sm flex items-center gap-2">
<i class="ph ph-plus"></i> Yangi bosqich
</a>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<table class="w-full text-left border-collapse">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4">Tartib</th>
<th class="p-4">Nomi</th>
<th class="p-4">Rang</th>
<th class="p-4">Lidlar soni</th>
<th class="p-4">Yutuq</th>
<th class="p-4 text-right">Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for stage in stages %}
<tr class="hover:bg-gray-50 transition-colors">
<td class="p-4 font-bold text-gray-600">{{ stage.order }}</td>
<td class="p-4">
<div class="flex items-center gap-3">
<span class="w-4 h-4 rounded-full" style="background-color: {{ stage.color }};"></span>
<span class="font-semibold text-gray-800">{{ stage.name }}</span>
</div>
</td>
<td class="p-4">
<span class="px-3 py-1 text-xs rounded-full font-medium"
style="background-color: {{ stage.color }}20; color: {{ stage.color }};">
{{ stage.color }}
</span>
</td>
<td class="p-4">
<span class="text-lg font-bold text-gray-800">{{ stage.lead_count }}</span>
<span class="text-gray-500 text-sm">lid</span>
</td>
<td class="p-4">
{% if stage.is_won %}
<span class="px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full font-medium">
<i class="ph ph-trophy"></i> Ha
</span>
{% else %}
<span class="text-gray-400">-</span>
{% endif %}
</td>
<td class="p-4 text-right">
<div class="flex items-center justify-end gap-2">
<a href="{% url 'stage_edit' stage.id %}"
class="p-2 text-gray-500 hover:text-blue-600 bg-gray-100 rounded-lg hover:bg-blue-50 transition">
<i class="ph ph-pencil-simple"></i>
</a>
<a href="{% url 'stage_delete' stage.id %}"
class="p-2 text-gray-500 hover:text-red-600 bg-gray-100 rounded-lg hover:bg-red-50 transition">
<i class="ph ph-trash"></i>
</a>
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="p-8 text-center text-gray-500">
<i class="ph ph-kanban text-4xl mb-2"></i>
<p>Hozircha bosqichlar yo'q. Yangi qo'shing!</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\dashboards\admin.html ---
{% extends 'base.html' %}
{% block title %}Boshqaruv Paneli{% endblock %}
{% block content %}
<div class="space-y-8">
<div class="flex items-center justify-between">
<div>
<h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
Xush kelibsiz, {{ request.user.first_name }}! 👋
</h1>
<p class="text-gray-500 mt-1">{{ organization.name|default:"Tashkilot" }} - Boshqaruv Paneli
</p>
</div>
<div
class="px-4 py-2 bg-white/50 backdrop-blur-sm rounded-xl text-sm font-medium text-gray-600 shadow-sm border border-white/60">
{% now "d F Y" %}
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<div
class="glass-panel p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
<div
class="absolute right-0 top-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-blue-500/20">
</div>
<div class="flex items-center justify-between relative">
<div>
<p class="text-sm font-medium text-gray-500">Jami O'quvchilar</p>
<p class="text-3xl font-bold text-gray-800 mt-2">{{ total_students }}</p>
<div class="flex items-center gap-1 mt-2">
<span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
<span class="text-xs text-green-600 font-medium">Aktiv</span>
</div>
</div>
<div
class="w-12 h-12 bg-blue-100/50 text-blue-600 rounded-2xl flex items-center justify-center text-2xl shadow-inner">
<i class="ph ph-student"></i>
</div>
</div>
</div>
<div
class="glass-panel p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
<div
class="absolute right-0 top-0 w-32 h-32 bg-orange-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-orange-500/20">
</div>
<div class="flex items-center justify-between relative">
<div>
<p class="text-sm font-medium text-gray-500">Yangi Lidlar</p>
<p class="text-3xl font-bold text-gray-800 mt-2">{{ total_leads }}</p>
<span
class="text-xs text-orange-600 bg-orange-50 px-2 py-1 rounded-full font-medium inline-block mt-2">
+{{ new_leads }} bugun
</span>
</div>
<div
class="w-12 h-12 bg-orange-100/50 text-orange-600 rounded-2xl flex items-center justify-center text-2xl shadow-inner">
<i class="ph ph-funnel"></i>
</div>
</div>
</div>
<div
class="glass-panel p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
<div
class="absolute right-0 top-0 w-32 h-32 bg-green-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-green-500/20">
</div>
<div class="flex items-center justify-between relative">
<div>
<p class="text-sm font-medium text-gray-500">Oylik Tushum</p>
<p class="text-3xl font-bold text-gray-800 mt-2">{{ monthly_income|floatformat:0 }}</p>
<span class="text-xs text-gray-400 mt-1 block">UZS</span>
</div>
<div
class="w-12 h-12 bg-green-100/50 text-green-600 rounded-2xl flex items-center justify-center text-2xl shadow-inner">
<i class="ph ph-wallet"></i>
</div>
</div>
</div>
<div
class="glass-panel p-6 rounded-2xl relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
<div
class="absolute right-0 top-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-red-500/20">
</div>
<div class="flex items-center justify-between relative">
<div>
<p class="text-sm font-medium text-gray-500">Qarzdorlik</p>
<p class="text-3xl font-bold text-red-600 mt-2">{{ total_debt|floatformat:0 }}</p>
<span class="text-xs text-red-600 bg-red-50 px-2 py-1 rounded-full font-medium inline-block mt-2">
Talab qilinadi
</span>
</div>
<div
class="w-12 h-12 bg-red-100/50 text-red-600 rounded-2xl flex items-center justify-center text-2xl shadow-inner">
<i class="ph ph-warning-circle"></i>
</div>
</div>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div
class="glass-panel p-6 rounded-2xl flex items-center justify-between hover:shadow-lg transition-all duration-300">
<div class="flex items-center gap-4">
<div
class="w-14 h-14 bg-indigo-100/50 text-indigo-600 rounded-2xl flex items-center justify-center text-3xl shadow-inner">
<i class="ph ph-users-three"></i>
</div>
<div>
<p class="text-sm font-medium text-gray-500">Aktiv Guruhlar</p>
<p class="text-2xl font-bold text-gray-800">{{ active_groups }}</p>
</div>
</div>
<i class="ph ph-caret-right text-gray-300"></i>
</div>
<div
class="glass-panel p-6 rounded-2xl flex items-center justify-between hover:shadow-lg transition-all duration-300">
<div class="flex items-center gap-4">
<div
class="w-14 h-14 bg-purple-100/50 text-purple-600 rounded-2xl flex items-center justify-center text-3xl shadow-inner">
<i class="ph ph-chalkboard-teacher"></i>
</div>
<div>
<p class="text-sm font-medium text-gray-500">O'qituvchilar</p>
<p class="text-2xl font-bold text-gray-800">{{ total_teachers }}</p>
</div>
</div>
<i class="ph ph-caret-right text-gray-300"></i>
</div>
</div>
{% if stages %}
<div class="glass-panel p-6 rounded-2xl">
<h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
<i class="ph ph-funnel-simple text-primary-500"></i> Sotuv Voronkasi
</h3>
<div class="flex gap-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-gray-200">
{% for stage in stages %}
<div class="flex-shrink-0 min-w-[200px] p-5 rounded-2xl border transition-all hover:shadow-md"
style="border-color: {{ stage.color }}; background: linear-gradient(145deg, #ffffff, {{ stage.color }}15);">
<div class="flex items-center gap-2 mb-3">
<span class="w-3 h-3 rounded-full shadow-sm"
style="background-color: {{ stage.color }}; box-shadow: 0 0 10px {{ stage.color }};"></span>
<span class="font-bold text-gray-700">{{ stage.name }}</span>
</div>
<div class="flex items-end justify-between">
<div>
<p class="text-3xl font-bold text-gray-800">{{ stage.lead_count }}</p>
<p class="text-xs text-gray-500 font-medium">lid mavjud</p>
</div>
<div style="color: {{ stage.color }}" class="opacity-50 text-3xl">
<i class="ph ph-user"></i>
</div>
</div>
</div>
{% endfor %}
</div>
{% endif %}
<div class="glass-panel p-6 rounded-2xl">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
<i class="ph ph-chart-line text-indigo-500"></i> Moliyaviy O'sish
</h3>
<div class="flex items-center gap-2">
<button onclick="loadChartData(7)"
class="px-3 py-1 text-xs rounded-lg bg-gray-100 dark:bg-dark-700 hover:bg-indigo-100 transition">7
kun</button>
<button onclick="loadChartData(30)"
class="px-3 py-1 text-xs rounded-lg bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600">30
kun</button>
<button onclick="loadChartData(90)"
class="px-3 py-1 text-xs rounded-lg bg-gray-100 dark:bg-dark-700 hover:bg-indigo-100 transition">90
kun</button>
</div>
</div>
<div class="h-64">
<canvas id="financeChart"></canvas>
</div>
</div>
<script>
let financeChart = null;
async function loadChartData(days = 30) {
const response = await fetch(`/api/chart-data/?days=${days}`);
const data = await response.json();
if (financeChart) {
financeChart.destroy();
}
const ctx = document.getElementById('financeChart').getContext('2d');
const isDark = document.documentElement.classList.contains('dark');
financeChart = new Chart(ctx, {
type: 'line',
data: {
labels: data.labels,
datasets: [
{
label: 'Kirim',
data: data.income,
borderColor: '#22c55e',
backgroundColor: 'rgba(34, 197, 94, 0.1)',
fill: true,
tension: 0.4,
pointRadius: 0,
},
{
label: 'Chiqim',
data: data.expense,
borderColor: '#ef4444',
backgroundColor: 'rgba(239, 68, 68, 0.1)',
fill: true,
tension: 0.4,
pointRadius: 0,
}
]
},
options: {
responsive: true,
maintainAspectRatio: false,
interaction: {
intersect: false,
mode: 'index'
},
plugins: {
legend: {
position: 'top',
labels: {
usePointStyle: true,
color: isDark ? '#e2e8f0' : '#374151'
}
}
},
scales: {
x: {
grid: { display: false },
ticks: { color: isDark ? '#94a3b8' : '#6b7280' }
},
y: {
grid: { color: isDark ? 'rgba(148,163,184,0.1)' : 'rgba(0,0,0,0.05)' },
ticks: {
color: isDark ? '#94a3b8' : '#6b7280',
callback: function (value) {
return value.toLocaleString('uz-UZ');
}
}
}
}
}
});
}
// Sahifa yuklanganda
document.addEventListener('DOMContentLoaded', () => loadChartData(30));
</script>
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 glass-panel p-6 rounded-2xl">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
<i class="ph ph-calendar-check text-green-500"></i> Bugungi Darslar
</h3>
<a href="{% url 'group_list' %}"
class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm text-gray-600 transition">
To'liq ko'rish
</a>
</div>
<div class="space-y-4">
{% for lesson in today_lessons %}
<div
class="flex items-center p-4 bg-white/50 rounded-xl border border-white hover:bg-white hover:shadow-md transition-all duration-300 group">
<div class="w-20 text-center border-r border-gray-100 pr-4">
<span
class="block text-lg font-bold text-gray-800 group-hover:text-primary-600 transition">{{
lesson.start_time|time:"H:i" }}</span>
<span class="block text-xs text-gray-400">{{ lesson.end_time|time:"H:i" }}</span>
</div>
<div class="flex-1 px-4">
<h4 class="font-bold text-gray-800 text-lg">{{ lesson.group.name }}</h4>
<p class="text-sm text-gray-500 flex items-center gap-3 mt-1">
<span class="flex items-center gap-1"><i class="ph ph-door text-gray-400"></i> {{
lesson.room.name|default:"-" }}</span>
<span class="flex items-center gap-1"><i class="ph ph-user text-gray-400"></i> {{
lesson.teacher.first_name|default:"-" }}</span>
</p>
</div>
<span class="px-3 py-1 text-xs font-bold rounded-full border
{% if lesson.status == 'started' %}text-blue-700 bg-blue-50 border-blue-100
{% elif lesson.status == 'finished' %}text-green-700 bg-green-50 border-green-100
{% else %}text-gray-600 bg-gray-50 border-gray-100{% endif %}">
{{ lesson.get_status_display }}
</span>
</div>
{% empty %}
<div class="text-center py-12 text-gray-400">
<div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="ph ph-calendar-blank text-4xl text-gray-300"></i>
</div>
<p class="font-medium">Bugun darslar yo'q</p>
</div>
{% endfor %}
</div>
</div>
<div class="glass-panel p-6 rounded-2xl flex flex-col h-full">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
<i class="ph ph-sparkle text-yellow-500"></i> So'nggi Lidlar
</h3>
<a href="{% url 'pipeline' %}" class="text-sm text-primary-600 hover:text-primary-700">Voronka</a>
</div>
<div class="space-y-4 flex-1 overflow-y-auto max-h-[400px] scrollbar-hide">
{% for lead in recent_leads %}
<div class="flex items-center gap-4 p-3 hover:bg-white/60 rounded-xl transition cursor-default">
<div
class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 text-white flex items-center justify-center font-bold text-lg shadow-md shadow-purple-500/20">
{{ lead.full_name|first }}
</div>
<div class="flex-1 min-w-0">
<h4 class="font-bold text-gray-800 truncate">{{ lead.full_name }}</h4>
<p class="text-xs text-gray-500 flex items-center gap-1">
<i class="ph ph-arrow-elbow-down-right"></i> {{ lead.source.name|default:"Noma'lum" }}
</p>
</div>
<div class="text-[10px] bg-gray-100 px-2 py-1 rounded text-gray-500 whitespace-nowrap">
{{ lead.created_at|timesince }}
</div>
</div>
{% empty %}
<div class="flex-1 flex flex-col items-center justify-center text-gray-400">
<p>Hozircha lidlar yo'q</p>
</div>
{% endfor %}
</div>
<a href="{% url 'lead_create' %}"
class="w-full mt-6 py-3 text-sm font-semibold text-center text-white bg-primary-600 rounded-xl hover:bg-primary-700 shadow-lg shadow-primary-600/30 transition-all active:scale-95 flex items-center justify-center gap-2">
<i class="ph ph-plus-circle text-lg"></i> Yangi Lid
</a>
</div>
</div>
</div>
{% endblock %}

--- templates\dashboards\parent.html ---
{% extends 'base.html' %}
{% block title %}Ota-ona Kabineti{% endblock %}
{% block content %}
<div class="space-y-8 animate-fadeIn">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-white flex items-center gap-3">
Assalomu alaykum, {{ request.user.first_name }}! 👨‍👩‍👧
<span class="icon-box-lg icon-blue">
<i class="ph-fill ph-users"></i>
</span>
</h1>
<p class="text-slate-400 mt-1">Ota-ona kabineti - Farzandlaringiz nazorati</p>
</div>
<div class="flex flex-wrap items-center gap-3">
{% if has_any_debt %}
<a href="{% url 'finance:add_income' %}" class="btn btn-danger">
<i class="ph-fill ph-credit-card"></i>
To'lov qilish
<span class="px-2 py-0.5 bg-white/20 rounded-full text-xs font-bold">{{ total_debt|floatformat:0 }}
so'm</span>
</a>
{% endif %}
<button onclick="openChatModal()" class="btn btn-primary">
<i class="ph-fill ph-chat-circle-dots"></i>
Administrator bilan gaplashish
</button>
<div class="px-4 py-2 bg-[#152642] rounded-xl text-sm font-medium text-slate-300 border border-[#1c3255]">
{% now "d F Y" %}
</div>
</div>
</div>
{% if children_data %}
<div class="space-y-8">
{% for data in children_data %}
<div class="card overflow-hidden transition hover:shadow-lg duration-300 p-0">
<div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-white relative overflow-hidden">
<div class="absolute right-0 top-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20"></div>
<div class="flex items-center gap-6 relative z-10">
<div
class="w-20 h-20 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center text-3xl font-bold shadow-inner border border-white/30">
{{ data.child.first_name|first }}
</div>
<div>
<h2 class="text-3xl font-bold mb-1">{{ data.child.first_name }} {{ data.child.last_name }}</h2>
<div class="flex items-center gap-4 text-blue-100 text-sm font-medium">
<span class="bg-white/20 px-3 py-1 rounded-lg backdrop-blur-sm">{{ data.relation_type
}}</span>
<span class="flex items-center gap-1"><i class="ph ph-phone"></i> {{ data.child.phone
}}</span>
</div>
</div>
</div>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 border-b border-[#1c3255] bg-[#152642]">
<div class="text-center p-4 rounded-xl hover:bg-[#0f1f35] transition duration-200">
<div
class="inline-flex items-center justify-center w-10 h-10 mb-2 rounded-full bg-emerald-500/20 text-emerald-400">
<i class="ph-fill ph-check-circle text-xl"></i>
</div>
<p class="text-3xl font-bold text-white">{{ data.attendance_rate }}%</p>
<p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Davomat</p>
</div>
<div class="text-center p-4 rounded-xl hover:bg-[#0f1f35] transition duration-200">
<div
class="inline-flex items-center justify-center w-10 h-10 mb-2 rounded-full bg-blue-500/20 text-blue-400">
<i class="ph-fill ph-star text-xl"></i>
</div>
<p class="text-3xl font-bold text-white">{{ data.avg_grade }}</p>
<p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">O'rtacha Baho</p>
</div>
<div class="text-center p-4 rounded-xl hover:bg-[#0f1f35] transition duration-200">
<div
class="inline-flex items-center justify-center w-10 h-10 mb-2 rounded-full bg-purple-500/20 text-purple-400">
<i class="ph-fill ph-lightning text-xl"></i>
</div>
<p class="text-3xl font-bold text-white">{{ data.xp }}</p>
<p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">XP Ochko</p>
</div>
<div class="text-center p-4 rounded-xl hover:bg-[#0f1f35] transition duration-200">
<div
class="inline-flex items-center justify-center w-10 h-10 mb-2 rounded-full {% if data.balance < 0 %}bg-rose-500/20 text-rose-400{% else %}bg-slate-500/20 text-slate-400{% endif %}">
<i class="ph-fill ph-wallet text-xl"></i>
</div>
<p class="text-3xl font-bold {% if data.balance < 0 %}text-rose-400{% else %}text-white{% endif %}">
{{ data.balance|floatformat:0 }}
</p>
<p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Balans (UZS)</p>
</div>
</div>
<div class="p-8 bg-[#0f1f35]">
<h3 class="font-bold text-white mb-6 flex items-center gap-2 text-lg">
<i class="ph-fill ph-books text-blue-400"></i> O'qiyotgan Guruhlari
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
{% for enrollment in data.enrollments %}
<div
class="flex items-center gap-4 p-5 bg-[#152642] border border-[#1c3255] rounded-xl hover:border-blue-500/50 transition duration-300">
<div
class="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-md shadow-blue-500/20">
{{ enrollment.group.course.name|first }}
</div>
<div class="flex-1">
<h4 class="font-bold text-white text-lg">{{ enrollment.group.name }}</h4>
<p class="text-sm font-medium text-slate-400">{{ enrollment.group.course.name }}</p>
<p class="text-xs text-slate-500 mt-1 flex items-center gap-1">
<i class="ph-fill ph-chalkboard-teacher"></i> {{ enrollment.group.teacher.first_name }}
</p>
</div>
</div>
{% empty %}
<p class="text-slate-500 col-span-2 text-center py-8 italic">Hozircha guruhlarga yozilmagan</p>
{% endfor %}
</div>
</div>
<div class="p-8 border-t border-[#1c3255] bg-[#152642]">
<h3 class="font-bold text-white mb-6 flex items-center gap-2 text-lg">
<i class="ph-fill ph-chart-line-up text-blue-400"></i> So'nggi Davomatlar
</h3>
<div class="flex flex-wrap gap-3">
{% for att in data.recent_attendance %}
<div class="flex flex-col items-center justify-center w-20 p-2 rounded-xl border transition-all hover:scale-105
{% if att.status == 'present' %}bg-emerald-500/10 text-emerald-400 border-emerald-500/30
{% elif att.status == 'absent' %}bg-rose-500/10 text-rose-400 border-rose-500/30
{% elif att.status == 'late' %}bg-amber-500/10 text-amber-400 border-amber-500/30
{% else %}bg-slate-500/10 text-slate-400 border-slate-500/30{% endif %}">
<span class="text-xs font-bold mb-1">{{ att.lesson.date|date:"d.m" }}</span>
<span class="text-2xl mb-1">
{% if att.status == 'present' %}<i class="ph-fill ph-check"></i>
{% elif att.status == 'absent' %}<i class="ph-fill ph-x"></i>
{% elif att.status == 'late' %}<i class="ph-fill ph-clock"></i>
{% else %}-{% endif %}
</span>
{% if att.grade %}
<span class="text-[10px] font-bold bg-white/10 px-1.5 rounded">{{ att.grade }}</span>
{% endif %}
</div>
{% empty %}
<p class="text-slate-500 italic">Hozircha davomat yo'q</p>
{% endfor %}
</div>
</div>
</div>
{% endfor %}
</div>
{% else %}
<div class="card p-16 text-center">
<div class="w-24 h-24 bg-[#152642] rounded-full flex items-center justify-center mx-auto mb-6">
<i class="ph ph-users text-5xl text-slate-500"></i>
</div>
<h3 class="text-2xl font-bold text-white mb-2">Farzandlar topilmadi</h3>
<p class="text-slate-400 max-w-md mx-auto">Sizga hech qanday o'quvchi biriktirilmagan. Iltimos, o'quv markazi
ma'muriyati bilan bog'laning.</p>
</div>
{% endif %}
</div>
<div id="chatModal" class="fixed inset-0 z-50 hidden">
<div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick="closeChatModal()"></div>
<div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-lg">
<div class="bg-[#0f1f35] border border-[#1c3255] rounded-2xl shadow-2xl overflow-hidden">
<div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 text-white flex items-center justify-between">
<div class="flex items-center gap-3">
<div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
<i class="ph-fill ph-chat-circle-text text-xl"></i>
</div>
<div>
<h3 class="font-bold">Bog'lanish</h3>
<p class="text-xs text-blue-100">Admin/O'qituvchi bilan</p>
</div>
</div>
<button onclick="closeChatModal()" class="p-2 hover:bg-white/20 rounded-lg transition">
<i class="ph ph-x text-xl"></i>
</button>
</div>
<div class="p-6">
<div class="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4 text-center">
<i class="ph-fill ph-info text-4xl text-blue-400 mb-3"></i>
<h4 class="font-bold text-white mb-2">Tez orada mavjud!</h4>
<p class="text-sm text-slate-400">
Chat funksiyasi ishlab chiqilmoqda. Hozircha telefon orqali bog'laning.
</p>
</div>
<div class="mt-4 p-4 bg-[#152642] rounded-xl">
<p class="text-xs text-slate-500 uppercase mb-2">Bog'lanish</p>
<p class="font-semibold text-white flex items-center gap-2">
<i class="ph-fill ph-phone text-emerald-400"></i> +998 90 123 45 67
</p>
</div>
</div>
</div>
</div>
</div>
<script>
function openChatModal() {
document.getElementById('chatModal').classList.remove('hidden');
}
function closeChatModal() {
document.getElementById('chatModal').classList.add('hidden');
}
</script>
{% endblock %}

--- templates\dashboards\staff.html ---
{% extends 'base.html' %}
{% block title %}Xodim Kabineti{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Xush kelibsiz, {{ request.user.first_name }}! 👋</h1>
<p class="text-gray-500">Xodim kabineti</p>
</div>
<div class="text-sm text-gray-500">{% now "d F Y" %}</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<div class="flex items-center gap-6">
<div
class="w-20 h-20 bg-gradient-to-br from-gray-400 to-gray-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
{{ request.user.first_name|first }}
</div>
<div>
<h2 class="text-xl font-bold text-gray-800">{{ request.user.first_name }} {{ request.user.last_name }}
</h2>
<p class="text-gray-500">{{ request.user.get_role_display }}</p>
<p class="text-sm text-gray-400">{{ request.user.phone }}</p>
</div>
</div>
</div>
<div class="bg-blue-50 border border-blue-200 rounded-xl p-6 text-center">
<i class="ph ph-info text-4xl text-blue-500 mb-2"></i>
<p class="text-blue-700">Sizning rolingiz uchun maxsus funksiyalar mavjud emas. Qo'shimcha huquqlar uchun
administratorga murojaat qiling.</p>
</div>
</div>
{% endblock %}

--- templates\dashboards\student.html ---
{% extends 'base.html' %}
{% block title %}Mening Kabinetim{% endblock %}
{% block content %}
<div class="space-y-8 animate-fadeIn">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-white flex items-center gap-3">
Salom, {{ request.user.first_name }}! 🎓
<span class="icon-box-lg icon-purple">
<i class="ph-fill ph-student"></i>
</span>
</h1>
<p class="text-slate-400 mt-1">O'quvchi shaxsiy kabineti</p>
</div>
<div class="px-4 py-2 bg-[#152642] rounded-xl text-sm font-medium text-slate-300 border border-[#1c3255]">
{% now "d F Y" %}
</div>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
<div class="stat-card hover-lift">
<div class="flex items-center justify-between mb-2">
<p class="text-xs font-semibold text-slate-400 uppercase">Davomat</p>
<i class="ph-fill ph-check-circle text-xl text-emerald-400"></i>
</div>
<p class="text-3xl font-bold text-white">{{ attendance_rate }}%</p>
<div class="w-full bg-[#0f1f35] rounded-full h-1.5 mt-3">
<div class="bg-emerald-500 h-1.5 rounded-full" style="width: {{ attendance_rate }}%"></div>
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex items-center justify-between mb-2">
<p class="text-xs font-semibold text-slate-400 uppercase">O'rtacha Baho</p>
<i class="ph-fill ph-star text-xl text-blue-400"></i>
</div>
<p class="text-3xl font-bold text-white">{{ avg_grade }}</p>
<div class="flex gap-0.5 mt-3 text-amber-400 text-xs">
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star-half"></i>
</div>
</div>
<div class="stat-card hover-lift bg-gradient-to-br from-amber-500/10 to-yellow-500/10 border-amber-500/30">
<div class="flex items-center justify-between mb-2">
<p class="text-xs font-semibold text-amber-400 uppercase">💰 Coin Balans</p>
{% if student_rank > 0 %}
<span class="px-2 py-0.5 bg-amber-500 text-white text-xs font-bold rounded-full">#{{ student_rank
}}</span>
{% endif %}
</div>
<p class="text-3xl font-bold text-amber-400">{{ coin_balance|default:total_xp }}</p>
<div class="flex items-center gap-2 mt-2">
<span class="text-xs text-purple-400 font-medium flex items-center gap-1">
<i class="ph-fill ph-lightning"></i> {{ total_xp }} XP
</span>
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex items-center justify-between mb-2">
<p class="text-xs font-semibold text-slate-400 uppercase">Balans</p>
<i class="ph-fill ph-wallet text-xl text-slate-400"></i>
</div>
<p class="text-3xl font-bold {% if balance < 0 %}text-rose-400{% else %}text-white{% endif %}">
{{ balance|floatformat:0 }}
</p>
<p class="text-xs text-slate-500 mt-2">UZS</p>
</div>
</div>
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 card">
<div class="flex items-center justify-between mb-6">
<h3 class="text-lg font-bold text-white flex items-center gap-2">
<i class="ph-fill ph-trophy text-amber-400"></i> Top 10 - Eng Faol O'quvchilar
</h3>
{% if student_rank > 0 %}
<span class="badge badge-amber">Sizning o'rningiz: #{{ student_rank }}</span>
{% endif %}
</div>
<div class="space-y-2 max-h-80 overflow-y-auto">
{% for s in leaderboard %}
<div
class="flex items-center justify-between p-3 rounded-xl transition {% if s.id == request.user.id %}bg-amber-500/10 border border-amber-500/30{% else %}hover:bg-[#152642]{% endif %}">
<div class="flex items-center gap-4">
<div class="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-lg
{% if forloop.counter == 1 %}bg-gradient-to-br from-amber-400 to-yellow-500 text-white shadow-lg shadow-amber-500/30
{% elif forloop.counter == 2 %}bg-gradient-to-br from-gray-300 to-gray-400 text-white
{% elif forloop.counter == 3 %}bg-gradient-to-br from-amber-600 to-orange-500 text-white
{% else %}bg-[#152642] text-slate-400{% endif %}">
{{ forloop.counter }}
</div>
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/30">
{{ s.first_name|first|default:"?" }}
</div>
<div>
<h4 class="font-semibold text-white">{{ s.first_name }} {{ s.last_name }}</h4>
{% if s.id == request.user.id %}
<span class="text-xs text-amber-400 font-medium">Bu sizsiz! 🎉</span>
{% endif %}
</div>
</div>
</div>
<div class="text-right">
<span class="text-lg font-bold text-purple-400">{{ s.xp_total|default:0 }}</span>
<span class="text-xs text-slate-500 ml-1">XP</span>
</div>
</div>
{% empty %}
<div class="text-center py-8 text-slate-400">
<i class="ph ph-users text-4xl text-slate-600 mb-2"></i>
<p class="font-medium">Hozircha reyting ma'lumotlari yo'q</p>
</div>
{% endfor %}
</div>
</div>
<div class="flex flex-col gap-6">
<a href="{% url 'operations:shop' %}"
class="card bg-gradient-to-br from-emerald-600 to-teal-700 border-emerald-500/30 hover:scale-[1.02] transition">
<div class="flex items-center justify-between mb-4">
<div
class="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center text-3xl backdrop-blur-sm">
🎁
</div>
{% if shop_items_count > 0 %}
<span class="px-3 py-1 bg-white/30 rounded-full text-sm font-bold text-white backdrop-blur-sm">
{{ shop_items_count }} ta mahsulot
</span>
{% endif %}
</div>
<h3 class="text-xl font-bold text-white mb-1">Do'konga kirish</h3>
<p class="text-emerald-200 text-sm">Coin sarflab sovg'alar oling!</p>
<div class="mt-4 flex items-center gap-2">
<span class="text-amber-300 font-bold text-lg">{{ coin_balance|default:total_xp }} 💰</span>
<span class="text-xs text-white/70">mavjud</span>
</div>
</a>
<div class="card">
<h4 class="text-sm font-bold text-slate-400 mb-4 uppercase">Tezkor statistika</h4>
<div class="space-y-3">
<div class="flex items-center justify-between">
<span class="text-sm text-slate-400">Davomat</span>
<span class="font-bold text-emerald-400">{{ attendance_rate }}%</span>
</div>
<div class="flex items-center justify-between">
<span class="text-sm text-slate-400">O'rtacha baho</span>
<span class="font-bold text-blue-400">{{ avg_grade }}</span>
</div>
<div class="flex items-center justify-between">
<span class="text-sm text-slate-400">Guruhlar</span>
<span class="font-bold text-purple-400">{{ my_enrollments|length }}</span>
</div>
</div>
</div>
</div>
</div>
<div class="card">
<div class="flex items-center justify-between mb-4">
<h3 class="text-xl font-bold text-white flex items-center gap-2">
<i class="ph-fill ph-trend-up text-blue-400"></i> O'zlashtirish Tarixi
</h3>
</div>
<div class="h-64 w-full">
<canvas id="gradesChart"></canvas>
</div>
</div>
<script>
document.addEventListener('DOMContentLoaded', function () {
const ctx = document.getElementById('gradesChart').getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(59, 130, 246, 0.3)');
gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');
new Chart(ctx, {
type: 'line',
data: {
labels: {{ chart_labels| safe }},
datasets: [{
label: 'Baho',
data: {{ chart_data| safe }},
borderColor: '#3b82f6',
backgroundColor: gradient,
borderWidth: 3,
tension: 0.4,
fill: true,
pointBackgroundColor: '#0f1f35',
pointBorderColor: '#3b82f6',
pointBorderWidth: 2,
pointRadius: 6,
pointHoverRadius: 8
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
plugins: {
legend: { display: false },
tooltip: {
backgroundColor: 'rgba(15, 31, 53, 0.95)',
borderColor: '#1c3255',
borderWidth: 1,
padding: 12,
cornerRadius: 8,
displayColors: false,
}
},
scales: {
y: {
beginAtZero: true,
max: 100,
grid: { color: 'rgba(28, 50, 85, 0.5)', borderDash: [5, 5] },
ticks: { color: '#64748b' }
},
x: {
grid: { display: false },
ticks: { color: '#64748b' }
}
}
}
});
});
</script>
<div class="card">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-calendar-check text-blue-400"></i> Bugungi Darslarim
</h3>
{% if today_lessons %}
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
{% for lesson in today_lessons %}
<div class="p-5 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-700 text-white shadow-lg">
<div class="flex items-start justify-between">
<div>
<span
class="inline-block px-2 py-1 bg-white/20 rounded-lg text-xs font-medium backdrop-blur-sm mb-2">
{{ lesson.start_time|time:"H:i" }} - {{ lesson.end_time|time:"H:i" }}
</span>
<h4 class="text-2xl font-bold mb-1">{{ lesson.group.name }}</h4>
<p class="text-blue-200 text-sm flex items-center gap-2">
<i class="ph-fill ph-chalkboard-teacher"></i> {{ lesson.teacher.first_name }} {{
lesson.teacher.last_name }}
</p>
</div>
<div
class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl backdrop-blur-sm">
<i class="ph-fill ph-book-open"></i>
</div>
</div>
<div class="mt-4 pt-4 border-t border-white/10 flex items-center justify-between">
<p class="text-xs text-blue-200 flex items-center gap-1">
<i class="ph ph-door"></i> {{ lesson.room.name|default:"Xona yo'q" }}
</p>
<span class="px-2 py-0.5 text-[10px] font-bold uppercase bg-white text-blue-600 rounded">
{{ lesson.get_status_display }}
</span>
</div>
</div>
{% endfor %}
</div>
{% else %}
<div class="text-center py-12 text-slate-400 bg-[#152642] rounded-xl border border-dashed border-[#1c3255]">
<div class="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-3">
<i class="ph-fill ph-sun text-3xl text-amber-400"></i>
</div>
<p class="font-medium text-white">Bugun darslaringiz yo'q!</p>
</div>
{% endif %}
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
<div class="card flex flex-col h-full">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-books text-blue-400"></i> Mening Kurslarim
</h3>
<div class="space-y-4 flex-1">
{% for enrollment in my_enrollments %}
<div
class="p-4 bg-[#152642] border border-[#1c3255] rounded-xl hover:border-blue-500/50 transition group">
<div class="flex items-center gap-4">
<div
class="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-md shadow-blue-500/20 group-hover:rotate-6 transition-transform">
{{ enrollment.group.course.name|first }}
</div>
<div class="flex-1">
<h4 class="font-bold text-white text-lg">{{ enrollment.group.name }}</h4>
<p class="text-xs text-slate-500 bg-[#0f1f35] px-2 py-0.5 rounded inline-block mt-1">{{
enrollment.group.course.name }}</p>
</div>
<div class="text-right">
<span class="px-2.5 py-1 text-xs font-bold rounded-lg border
{% if enrollment.status == 'active' %}bg-emerald-500/20 text-emerald-400 border-emerald-500/30
{% elif enrollment.status == 'frozen' %}bg-blue-500/20 text-blue-400 border-blue-500/30
{% else %}bg-slate-500/20 text-slate-400 border-slate-500/30{% endif %}">
{{ enrollment.get_status_display }}
</span>
</div>
</div>
</div>
{% empty %}
<div class="flex-1 flex items-center justify-center text-slate-400 py-8">
<p>Hozircha guruhlarga yozilmagansiz</p>
</div>
{% endfor %}
</div>
</div>
<div class="card flex flex-col h-full">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-chart-bar text-purple-400"></i> So'nggi Davomatlar
</h3>
<div class="space-y-3 flex-1 overflow-y-auto max-h-[400px] pr-2">
{% for att in my_attendance %}
<div class="flex items-center justify-between p-3 hover:bg-[#152642] rounded-xl transition">
<div class="flex items-center gap-4">
<div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg
{% if att.status == 'present' %}bg-emerald-500/20 text-emerald-400
{% elif att.status == 'absent' %}bg-rose-500/20 text-rose-400
{% elif att.status == 'late' %}bg-amber-500/20 text-amber-400
{% else %}bg-slate-500/20 text-slate-400{% endif %}">
{% if att.status == 'present' %}<i class="ph-fill ph-check"></i>
{% elif att.status == 'absent' %}<i class="ph-fill ph-x"></i>
{% elif att.status == 'late' %}<i class="ph-fill ph-clock"></i>
{% else %}<i class="ph-fill ph-minus"></i>{% endif %}
</div>
<div>
<p class="font-bold text-white text-sm">{{ att.lesson.group.name }}</p>
<p class="text-[10px] text-slate-500 font-medium uppercase">{{ att.lesson.date|date:"d M Y"
}}</p>
</div>
</div>
<div class="text-right flex flex-col items-end">
{% if att.grade %}
<div class="flex items-baseline gap-0.5">
<span class="text-lg font-bold text-blue-400">{{ att.grade }}</span>
<span class="text-[10px] text-slate-500">/100</span>
</div>
{% endif %}
{% if att.xp_points > 0 %}
<span
class="text-[10px] font-bold text-white bg-gradient-to-r from-purple-500 to-pink-500 px-1.5 py-0.5 rounded shadow-sm shadow-purple-500/30">+{{
att.xp_points }} XP</span>
{% endif %}
</div>
</div>
{% empty %}
<div class="flex-1 flex items-center justify-center text-slate-400 py-8">
<p>Hozircha davomat yo'q</p>
</div>
{% endfor %}
</div>
</div>
</div>
{% if upcoming_lessons %}
<div class="card">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-calendar text-amber-400"></i> Kelasi Darslar
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
{% for lesson in upcoming_lessons %}
<div class="p-5 bg-[#152642] border border-[#1c3255] rounded-xl hover:border-blue-500/50 transition">
<div class="text-xs font-bold text-amber-400 bg-amber-500/10 px-2 py-1 rounded-md inline-block mb-3">{{
lesson.date|date:"d M, l" }}</div>
<div class="text-2xl font-bold text-white mb-1">{{ lesson.start_time|time:"H:i" }}</div>
<p class="text-sm font-semibold text-slate-300">{{ lesson.group.name }}</p>
<p class="text-xs text-slate-500 mt-2 flex items-center gap-1"><i class="ph ph-door"></i> {{
lesson.room.name|default:"-" }}</p>
</div>
{% endfor %}
</div>
</div>
{% endif %}
{% if payments %}
<div class="card">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-receipt text-cyan-400"></i> To'lovlar Tarixi
</h3>
<div class="overflow-x-auto">
<table class="w-full table-dark">
<thead>
<tr>
<th class="rounded-l-xl">Sana</th>
<th>Turi</th>
<th class="text-right">Summa</th>
<th class="text-center rounded-r-xl">Holat</th>
</tr>
</thead>
<tbody>
{% for payment in payments %}
<tr>
<td class="text-sm font-medium">{{ payment.created_at|date:"d.m.Y" }}</td>
<td class="text-sm">{{ payment.get_transaction_type_display }}</td>
<td
class="text-right font-bold
{% if payment.transaction_type == 'income' %}text-emerald-400{% else %}text-rose-400{% endif %}">
{% if payment.transaction_type == 'income' %}+{% else %}-{% endif %} {{
payment.amount|floatformat:0 }}
</td>
<td class="text-center">
<span class="px-2.5 py-1 text-xs font-bold rounded-lg
{% if payment.status == 'confirmed' %}bg-emerald-500/20 text-emerald-400 border border-emerald-500/30
{% elif payment.status == 'pending' %}bg-amber-500/20 text-amber-400 border border-amber-500/30
{% else %}bg-rose-500/20 text-rose-400 border border-rose-500/30{% endif %}">
{{ payment.get_status_display }}
</span>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endif %}
</div>
{% endblock %}

--- templates\dashboards\super_admin.html ---
{% extends 'base.html' %}
{% block title %}Super Admin Panel{% endblock %}
{% block content %}
<div class="space-y-8 animate-fadeIn">
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
<div>
<h2 class="text-2xl font-bold text-white flex items-center gap-3">
Super Admin Panel
<span class="icon-box-lg icon-blue">
<i class="ph-fill ph-shield-check"></i>
</span>
</h2>
<p class="text-slate-400 text-sm mt-1 flex items-center gap-2">
<i class="ph ph-calendar-dots"></i>
Butun tizim statistikasi - {% now "d F Y" %}
</p>
</div>
<div class="flex flex-wrap gap-3">
<a href="{% url 'user_create' %}" class="btn btn-success">
<i class="ph-fill ph-user-plus"></i> O'quvchi qo'shish
</a>
<a href="{% url 'finance:add_income' %}" class="btn btn-primary">
<i class="ph-fill ph-plus-circle"></i> To'lov qabul
</a>
<a href="{% url 'lead_create' %}" class="btn btn-ghost">
<i class="ph-fill ph-funnel"></i> Lid qo'shish
</a>
</div>
</div>
<div class="flex items-center justify-between">
<h3 class="text-lg font-semibold text-white flex items-center gap-2">
<span class="w-1 h-6 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></span>
Moliya Statistikasi
</h3>
<div class="flex gap-1 bg-[#152642] p-1 rounded-xl">
<a href="?period=weekly"
class="px-4 py-2 rounded-lg text-sm font-medium transition {% if period == 'weekly' %}bg-blue-500 text-white{% else %}text-slate-400 hover:text-white{% endif %}">
Haftalik
</a>
<a href="?period=monthly"
class="px-4 py-2 rounded-lg text-sm font-medium transition {% if period != 'weekly' %}bg-blue-500 text-white{% else %}text-slate-400 hover:text-white{% endif %}">
Oylik
</a>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<div class="stat-card hover-lift">
<div class="flex justify-between items-start mb-4">
<div>
<p class="text-slate-400 text-sm font-medium uppercase tracking-wide">Bugungi Kirim</p>
<h3 class="text-3xl font-bold text-white mt-2">{{ today_income|floatformat:0|default:"0" }}</h3>
<p class="text-xs text-slate-500 mt-1">so'm</p>
</div>
<div class="icon-box-lg icon-green">
<i class="ph-fill ph-arrow-down-left"></i>
</div>
</div>
<div class="flex items-center gap-2 text-emerald-400 text-sm">
<i class="ph-fill ph-trend-up"></i>
Tushum
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex justify-between items-start mb-4">
<div>
<p class="text-slate-400 text-sm font-medium uppercase tracking-wide">Bugungi Chiqim</p>
<h3 class="text-3xl font-bold text-white mt-2">{{ today_expense|floatformat:0|default:"0" }}</h3>
<p class="text-xs text-slate-500 mt-1">so'm</p>
</div>
<div class="icon-box-lg icon-rose">
<i class="ph-fill ph-arrow-up-right"></i>
</div>
</div>
<div class="flex items-center gap-2 text-rose-400 text-sm">
<i class="ph-fill ph-trend-down"></i>
Xarajat
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex justify-between items-start mb-4">
<div>
<p class="text-slate-400 text-sm font-medium uppercase tracking-wide">Oylik Sof Foyda</p>
<h3 class="text-3xl font-bold text-white mt-2">{{ net_profit|floatformat:0|default:"0" }}</h3>
<p class="text-xs text-slate-500 mt-1">so'm</p>
</div>
<div class="icon-box-lg icon-blue">
<i class="ph-fill ph-chart-line-up"></i>
</div>
</div>
<div class="flex gap-2 text-xs">
<span class="badge badge-green">+{{ period_income|floatformat:0 }}</span>
<span class="badge badge-rose">-{{ period_expense|floatformat:0 }}</span>
</div>
</div>
<a href="{% url 'user_list' %}?filter=debtors" class="stat-card hover-lift cursor-pointer group">
<div class="flex justify-between items-start mb-4">
<div>
<p class="text-slate-400 text-sm font-medium uppercase tracking-wide">Qarzdorlik</p>
<h3 class="text-3xl font-bold text-amber-400 mt-2">{{ total_debt|floatformat:0|default:"0" }}</h3>
<p class="text-xs text-slate-500 mt-1">so'm</p>
</div>
<div class="icon-box-lg icon-amber animate-pulse-glow">
<i class="ph-fill ph-warning-circle"></i>
</div>
</div>
<div class="flex items-center gap-2 text-amber-400 text-sm">
<i class="ph-fill ph-users"></i>
{{ debtors_count|default:"0" }} nafar qarzdor
</div>
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="premium-card hover-lift">
<div class="flex justify-between items-center mb-6">
<h4 class="text-lg font-semibold text-white">O'quvchilar</h4>
<div class="icon-box-lg icon-purple">
<i class="ph-fill ph-student"></i>
</div>
</div>
<h2 class="text-4xl font-bold text-gradient-purple mb-4">{{ total_students|default:"0" }}</h2>
<div class="flex gap-3 text-sm">
<span class="badge badge-green">
<span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-1.5 animate-pulse"></span>
{{ active_students|default:"0" }} faol
</span>
<span class="badge badge-blue">
<span class="w-1.5 h-1.5 bg-blue-400 rounded-full mr-1.5"></span>
{{ frozen_students|default:"0" }} muzlatilgan
</span>
</div>
</div>
<div class="premium-card hover-lift">
<div class="flex justify-between items-center mb-6">
<h4 class="text-lg font-semibold text-white">Guruhlar</h4>
<div class="icon-box-lg icon-blue">
<i class="ph-fill ph-users-three"></i>
</div>
</div>
<h2 class="text-4xl font-bold text-gradient mb-4">{{ total_groups|default:"0" }}</h2>
<span class="badge badge-green">
<span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-1.5 animate-pulse"></span>
{{ active_groups|default:"0" }} faol guruh
</span>
</div>
<div class="premium-card hover-lift">
<div class="flex justify-between items-center mb-6">
<h4 class="text-lg font-semibold text-white">Bugungi Davomat</h4>
<div class="icon-box-lg icon-green">
<i class="ph-fill ph-check-circle"></i>
</div>
</div>
<h2 class="text-4xl font-bold text-emerald-400 mb-4">{{ attendance_rate|default:"0" }}%</h2>
<p class="text-sm text-slate-400">
<i class="ph ph-chalkboard-teacher mr-1"></i>
{{ finished_lessons|default:"0" }}/{{ total_today_lessons|default:"0" }} dars o'tildi
</p>
</div>
</div>
</div>
{% endblock %}

--- templates\dashboards\teacher.html ---
{% extends 'base.html' %}
{% block title %}O'qituvchi Paneli{% endblock %}
{% block content %}
<div class="space-y-8 animate-fadeIn">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-white flex items-center gap-3">
Salom, {{ request.user.first_name }}! 📚
<span class="icon-box-lg icon-purple">
<i class="ph-fill ph-chalkboard-teacher"></i>
</span>
</h1>
<p class="text-slate-400 mt-1">O'qituvchi boshqaruv paneli</p>
</div>
<div class="px-4 py-2 bg-[#152642] rounded-xl text-sm font-medium text-slate-300 border border-[#1c3255]">
{% now "d F Y, l" %}
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="stat-card hover-lift">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm font-medium uppercase">Mening Guruhlarim</p>
<p class="text-4xl font-bold text-white mt-2">{{ my_groups.count }}</p>
</div>
<div class="icon-box-lg icon-blue">
<i class="ph-fill ph-users-three"></i>
</div>
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm font-medium uppercase">Bugungi Darslar</p>
<p class="text-4xl font-bold text-white mt-2">{{ today_lessons.count }}</p>
</div>
<div class="icon-box-lg icon-green">
<i class="ph-fill ph-chalkboard"></i>
</div>
</div>
</div>
<div class="stat-card hover-lift">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm font-medium uppercase">Jami O'quvchilar</p>
<p class="text-4xl font-bold text-white mt-2">{{ total_students }}</p>
</div>
<div class="icon-box-lg icon-purple">
<i class="ph-fill ph-student"></i>
</div>
</div>
</div>
</div>
<div class="card">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-bold text-white flex items-center gap-2">
<i class="ph-fill ph-chart-line-up text-blue-400"></i> Oylik KPI
</h3>
<span class="badge badge-blue">{{ today|date:"F Y" }}</span>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
<div class="p-4 bg-[#152642] rounded-xl border border-[#1c3255]">
<div class="flex items-center justify-between mb-3">
<span class="text-xs font-semibold text-emerald-400 uppercase">Dars bajarish</span>
<div class="icon-box icon-green">
<i class="ph-fill ph-check-circle"></i>
</div>
</div>
<p class="text-3xl font-bold text-emerald-400">{{ lesson_completion_rate }}%</p>
<p class="text-xs text-slate-500 mt-1">{{ completed_lessons }}/{{ total_monthly_lessons }} dars</p>
</div>
<div class="p-4 bg-[#152642] rounded-xl border border-[#1c3255]">
<div class="flex items-center justify-between mb-3">
<span class="text-xs font-semibold text-blue-400 uppercase">O'quvchi davomati</span>
<div class="icon-box icon-blue">
<i class="ph-fill ph-users"></i>
</div>
</div>
<p class="text-3xl font-bold text-blue-400">{{ student_attendance_rate }}%</p>
<div class="w-full bg-[#0f1f35] rounded-full h-1.5 mt-2">
<div class="bg-blue-500 h-1.5 rounded-full" style="width: {{ student_attendance_rate }}%"></div>
</div>
</div>
<div class="p-4 bg-[#152642] rounded-xl border border-[#1c3255]">
<div class="flex items-center justify-between mb-3">
<span class="text-xs font-semibold text-amber-400 uppercase">O'rtacha baho</span>
<div class="icon-box icon-amber">
<i class="ph-fill ph-star"></i>
</div>
</div>
<p class="text-3xl font-bold text-amber-400">{{ avg_grade_given }}</p>
<div class="flex gap-0.5 mt-2 text-amber-400 text-xs">
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star"></i>
<i class="ph-fill ph-star-half"></i>
<i class="ph ph-star"></i>
</div>
</div>
<div class="p-4 bg-[#152642] rounded-xl border border-[#1c3255]">
<div class="flex items-center justify-between mb-3">
<span class="text-xs font-semibold text-purple-400 uppercase">XP berilgan</span>
<div class="icon-box icon-purple">
<i class="ph-fill ph-lightning"></i>
</div>
</div>
<p class="text-3xl font-bold text-purple-400">{{ total_xp_given }}</p>
<p class="text-xs text-slate-500 mt-1">Bu oyda</p>
</div>
</div>
</div>
<div class="card">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-bold text-white flex items-center gap-2">
<i class="ph-fill ph-calendar-check text-green-400"></i> Bugungi Darslarim
</h3>
<span class="badge badge-green">{{ today|date:"d F Y" }}</span>
</div>
{% if today_lessons %}
<div class="grid grid-cols-1 gap-4">
{% for lesson in today_lessons %}
<div
class="flex flex-col md:flex-row items-start md:items-center p-5 bg-[#152642] rounded-xl border border-[#1c3255] hover:border-blue-500/50 transition group">
<div class="flex items-center gap-4 md:w-32 mb-4 md:mb-0">
<div class="w-16 text-center bg-[#0f1f35] rounded-lg py-2 border border-[#1c3255]">
<span class="block text-lg font-bold text-white">{{ lesson.start_time|time:"H:i" }}</span>
<span class="block text-xs text-slate-500">{{ lesson.end_time|time:"H:i" }}</span>
</div>
</div>
<div class="hidden md:block w-px h-12 bg-[#1c3255] mx-6 relative">
<div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full
{% if lesson.status == 'started' %}bg-blue-500 ring-4 ring-blue-500/30
{% elif lesson.status == 'finished' %}bg-green-500 ring-4 ring-green-500/30
{% else %}bg-slate-400 ring-4 ring-slate-500/30{% endif %}"></div>
</div>
<div class="flex-1 min-w-0">
<h4 class="font-bold text-white text-lg group-hover:text-blue-400 transition">{{ lesson.group.name
}}</h4>
<p class="text-sm text-slate-400 flex items-center gap-4 mt-1">
<span class="flex items-center gap-1.5"><i class="ph ph-door"></i> {{
lesson.room.name|default:"Xona belgilanmagan" }}</span>
</p>
</div>
<div class="flex items-center gap-3 mt-4 md:mt-0">
<span class="px-3 py-1.5 text-xs font-bold rounded-full
{% if lesson.status == 'started' %}bg-blue-500/20 text-blue-400 border border-blue-500/30
{% elif lesson.status == 'finished' %}bg-green-500/20 text-green-400 border border-green-500/30
{% else %}bg-slate-500/20 text-slate-400 border border-slate-500/30{% endif %}">
{{ lesson.get_status_display }}
</span>
{% if lesson.status == 'scheduled' or lesson.status == 'started' %}
<a href="#" class="btn btn-primary">
<i class="ph-fill ph-check-circle"></i> Davomat
</a>
{% endif %}
</div>
</div>
{% endfor %}
</div>
{% else %}
<div class="text-center py-16 text-slate-400 bg-[#152642] rounded-2xl border border-dashed border-[#1c3255]">
<div class="w-20 h-20 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="ph-fill ph-sun text-4xl text-amber-400"></i>
</div>
<p class="text-lg font-medium text-white">Bugun darslaringiz yo'q!</p>
<p class="text-sm mt-1">Dam oling yoki keyingi darsga tayyorlaning</p>
</div>
{% endif %}
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
<div class="card flex flex-col h-full">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-users text-blue-400"></i> Mening Guruhlarim
</h3>
<div class="space-y-4 flex-1">
{% for group in my_groups %}
<div
class="flex items-center justify-between p-4 bg-[#152642] border border-[#1c3255] hover:border-blue-500/50 rounded-xl transition cursor-pointer group">
<div class="flex items-center gap-4">
<div
class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform">
{{ group.name|first }}
</div>
<div>
<h4 class="font-bold text-white group-hover:text-blue-400 transition">{{ group.name }}</h4>
<p
class="text-xs text-slate-500 font-medium bg-[#0f1f35] px-2 py-0.5 rounded-md inline-block mt-1">
{{ group.course.name }}</p>
</div>
</div>
<div class="text-right">
<p class="text-xl font-bold text-white">{{ group.student_count }}</p>
<p class="text-[10px] text-slate-500 font-medium uppercase tracking-wide">o'quvchi</p>
</div>
</div>
{% empty %}
<div class="flex-1 flex items-center justify-center text-slate-400 py-8">
<p>Hozircha guruhlar yo'q</p>
</div>
{% endfor %}
</div>
</div>
<div class="card flex flex-col h-full">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-clock-counter-clockwise text-amber-400"></i> Davomat kutilmoqda
</h3>
<div class="space-y-4 flex-1">
{% for lesson in pending_attendance %}
<div
class="flex items-center justify-between p-4 bg-amber-500/10 rounded-xl border border-amber-500/30">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 bg-amber-500/20 text-amber-400 rounded-lg flex items-center justify-center text-xl">
<i class="ph-fill ph-warning-circle"></i>
</div>
<div>
<h4 class="font-bold text-white">{{ lesson.group.name }}</h4>
<p class="text-xs text-slate-400 font-medium">{{ lesson.date|date:"d M Y" }}</p>
</div>
</div>
<a href="#" class="btn btn-ghost hover:bg-amber-500 hover:text-white hover:border-amber-500">
Belgilash
</a>
</div>
{% empty %}
<div class="flex-1 flex flex-col items-center justify-center text-slate-400 py-8">
<div class="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mb-3">
<i class="ph-fill ph-check-circle text-3xl text-green-400"></i>
</div>
<p class="font-medium text-white">Barcha davomatlar belgilangan!</p>
</div>
{% endfor %}
</div>
</div>
</div>
{% if upcoming_lessons %}
<div class="card">
<h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
<i class="ph-fill ph-calendar text-blue-400"></i> Keyingi Darslar
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
{% for lesson in upcoming_lessons %}
<div class="p-5 bg-[#152642] border border-[#1c3255] rounded-xl hover:border-blue-500/50 transition">
<div class="flex items-center justify-between mb-3">
<span class="text-sm font-bold text-blue-400 bg-blue-500/10 px-2 py-1 rounded-lg">{{
lesson.date|date:"d M" }}</span>
<span class="text-xs text-slate-500 font-medium flex items-center gap-1"><i class="ph ph-clock"></i>
{{ lesson.start_time|time:"H:i" }}</span>
</div>
<h4 class="font-bold text-white text-lg mb-1">{{ lesson.group.name }}</h4>
<p class="text-xs text-slate-500 flex items-center gap-1">
<i class="ph ph-door"></i> {{ lesson.room.name|default:"-" }}
</p>
</div>
{% endfor %}
</div>
</div>
{% endif %}
</div>
{% endblock %}

--- templates\education\course_list.html ---
{% extends 'base.html' %}
{% block content %}
<div class="space-y-6">
<div class="flex justify-between items-center">
<h1 class="text-2xl font-bold">Kurslar</h1>
<a href="{% url 'course_create' %}" class="btn-primary">+ Kurs qo'shish</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
{% for course in courses %}
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
<div class="flex justify-between items-start">
<div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center text-xl font-bold">
{{ course.name|first }}
</div>
{% if course.is_active %}
<span class="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full">Aktiv</span>
{% else %}
<span class="bg-red-100 text-red-700 text-xs px-2 py-1 rounded-full">Yopilgan</span>
{% endif %}
</div>
<h3 class="mt-4 text-lg font-bold text-gray-800">{{ course.name }}</h3>
<p class="text-gray-500 text-sm mt-1">{{ course.description|truncatechars:50 }}</p>
<div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
<span class="font-bold text-gray-800">{{ course.price }} UZS</span>
<span class="text-sm text-gray-500">{{ course.duration_months }} oy</span>
</div>
</div>
{% empty %}
<p class="text-gray-500">Kurslar yo'q.</p>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\education\form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="javascript:history.back()" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
</div>
<form method="POST" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
{% csrf_token %}
{{ form.as_p }}
<div class="flex justify-end gap-4 pt-4 border-t">
<a href="javascript:history.back()"
class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
Bekor qilish
</a>
<button type="submit" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 transition">
Saqlash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\education\group_detail.html ---
{% extends 'base.html' %}
{% block title %}{{ group.name }}{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'group_list' %}" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800">{{ group.name }}</h1>
<p class="text-gray-500">{{ group.course.name }}</p>
</div>
</div>
<div class="flex items-center gap-2">
<a href="{% url 'group_edit' group.pk %}"
class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition flex items-center gap-2">
<i class="ph ph-pencil"></i> Tahrirlash
</a>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
<div>
<p class="text-xs text-gray-500">O'qituvchi</p>
<p class="font-semibold text-gray-800">{{ group.teacher.first_name|default:"Belgilanmagan" }} {{
group.teacher.last_name|default:"" }}</p>
</div>
<div>
<p class="text-xs text-gray-500">Xona</p>
<p class="font-semibold text-gray-800">{{ group.room.name|default:"Belgilanmagan" }}</p>
</div>
<div>
<p class="text-xs text-gray-500">Vaqt</p>
<p class="font-semibold text-gray-800">
{{ group.start_time|time:"H:i"|default:"-" }} - {{ group.end_time|time:"H:i"|default:"-" }}
</p>
</div>
<div>
<p class="text-xs text-gray-500">Holat</p>
<span class="px-2 py-1 text-xs rounded-full font-medium
{% if group.status == 'active' %}bg-green-100 text-green-700
{% elif group.status == 'pending' %}bg-yellow-100 text-yellow-700
{% elif group.status == 'finished' %}bg-gray-100 text-gray-700
{% else %}bg-red-100 text-red-700{% endif %}">
{{ group.get_status_display }}
</span>
</div>
<div>
<p class="text-xs text-gray-500">Boshlanish</p>
<p class="font-semibold text-gray-800">{{ group.start_date|date:"d.m.Y"|default:"-" }}</p>
</div>
<div>
<p class="text-xs text-gray-500">Tugash</p>
<p class="font-semibold text-gray-800">{{ group.end_date|date:"d.m.Y"|default:"-" }}</p>
</div>
<div>
<p class="text-xs text-gray-500">Dars kunlari</p>
<p class="font-semibold text-gray-800">
{% for day in group.schedule_days %}
{% if day == 1 %}Du{% elif day == 2 %}Se{% elif day == 3 %}Ch{% elif day == 4 %}Pa{% elif day == 5
%}Ju{% elif day == 6 %}Sh{% elif day == 7 %}Ya{% endif %}{% if not forloop.last %}, {% endif %}
{% empty %}-{% endfor %}
</p>
</div>
<div>
<p class="text-xs text-gray-500">Narxi</p>
<p class="font-semibold text-gray-800">{{ group.course.price|floatformat:0 }} UZS</p>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<div class="p-4 bg-gray-50 border-b flex items-center justify-between">
<h3 class="font-bold text-gray-800">O'quvchilar</h3>
<span class="text-sm text-gray-500">{{ enrollments.count }} ta</span>
</div>
{% if available_students %}
<form method="POST" action="{% url 'add_student_to_group' group.pk %}"
class="p-4 bg-blue-50 border-b flex items-center gap-4">
{% csrf_token %}
<select name="student_id"
class="flex-1 px-4 py-2 rounded-lg border border-blue-200 focus:outline-none focus:ring-2 focus:ring-primary bg-white">
<option value="">O'quvchi tanlang...</option>
{% for student in available_students %}
<option value="{{ student.id }}">{{ student.first_name }} {{ student.last_name }} ({{ student.phone }})
</option>
{% endfor %}
</select>
<button type="submit"
class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2">
<i class="ph ph-plus"></i> Qo'shish
</button>
</form>
{% endif %}
<table class="w-full">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4 text-left">#</th>
<th class="p-4 text-left">O'quvchi</th>
<th class="p-4 text-left">Telefon</th>
<th class="p-4 text-center">Qo'shilgan</th>
<th class="p-4 text-center">Holat</th>
<th class="p-4 text-right">Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for e in enrollments %}
<tr class="hover:bg-gray-50 transition">
<td class="p-4 text-gray-500">{{ forloop.counter }}</td>
<td class="p-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 text-white flex items-center justify-center font-bold">
{{ e.student.first_name|first }}
</div>
<div>
<p class="font-semibold text-gray-800">{{ e.student.first_name }} {{ e.student.last_name
}}</p>
<p class="text-xs text-gray-500">ID: {{ e.student.id }}</p>
</div>
</div>
</td>
<td class="p-4 text-gray-600">{{ e.student.phone }}</td>
<td class="p-4 text-center text-sm text-gray-500">{{ e.joined_at|date:"d.m.Y" }}</td>
<td class="p-4 text-center">
<span class="px-2 py-1 text-xs rounded-full font-medium
{% if e.status == 'active' %}bg-green-100 text-green-700
{% elif e.status == 'frozen' %}bg-blue-100 text-blue-700
{% else %}bg-gray-100 text-gray-700{% endif %}">
{{ e.get_status_display }}
</span>
</td>
<td class="p-4 text-right">
<div class="flex items-center justify-end gap-2">
<a href="{% url 'finance:student_payments' e.student.id %}"
class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition" title="To'lovlar">
<i class="ph ph-wallet"></i>
</a>
<form method="POST" action="{% url 'remove_student_from_group' group.pk e.student.id %}"
class="inline" onsubmit="return confirm('Haqiqatan ham chiqarasizmi?');">
{% csrf_token %}
<button type="submit" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
title="Chiqarish">
<i class="ph ph-user-minus"></i>
</button>
</form>
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="p-8 text-center text-gray-500">
<i class="ph ph-users text-4xl mb-2"></i>
<p>Hozircha o'quvchilar yo'q</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\education\group_form.html ---
{% extends 'base.html' %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow-sm border border-gray-100">
<h2 class="text-xl font-bold mb-6">Yangi Guruh</h2>
{% if form.errors %}
<div class="bg-red-50 text-red-600 p-4 rounded-lg mb-4 text-sm">
{{ form.non_field_errors }}
{% for field in form %}
{% if field.errors %}
<p><b>{{ field.label }}:</b> {{ field.errors|striptags }}</p>
{% endif %}
{% endfor %}
</div>
{% endif %}
<form method="post" class="space-y-4">
{% csrf_token %}
<div class="grid grid-cols-2 gap-4">
<div><label>Nomi</label>{{ form.name }}</div>
<div><label>Holati</label>{{ form.status }}</div>
</div>
<div class="grid grid-cols-2 gap-4">
<div><label>Kurs</label>{{ form.course }}</div>
<div><label>O'qituvchi</label>{{ form.teacher }}</div>
</div>
<div class="grid grid-cols-3 gap-4">
<div><label>Xona</label>{{ form.room }}</div>
<div><label>Boshlanish</label>{{ form.start_time }}</div>
<div><label>Tugash</label>{{ form.end_time }}</div>
</div>
<div>
<label>Dars Kunlari (Ctrl bosib bir nechtasini tanlang)</label>
{{ form.schedule_days }}
<p class="text-xs text-gray-500 mt-1">1=Dushanba, ... 6=Shanba</p>
</div>
<div><label>Boshlanish Sanasi</label>{{ form.start_date }}</div>
<button type="submit" class="btn-primary w-full mt-4">Guruhni Saqlash</button>
</form>
</div>
<style>
label { display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem; }
.btn-primary {
background-color: #4F46E5; color: white; padding: 0.75rem; border-radius: 0.5rem; font-weight: bold;
}
</style>
{% endblock %}

--- templates\education\group_list.html ---
{% extends 'base.html' %}
{% block content %}
<div class="space-y-6">
<div class="flex justify-between items-center">
<h1 class="text-2xl font-bold">Guruhlar</h1>
<a href="{% url 'group_create' %}" class="btn-primary">+ Guruh yaratish</a>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<table class="w-full text-left">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs">
<tr>
<th class="p-4">Guruh nomi</th>
<th class="p-4">Kurs</th>
<th class="p-4">O'qituvchi</th>
<th class="p-4">Xona</th>
<th class="p-4">Vaqti</th>
<th class="p-4">Holati</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for group in groups %}
<tr class="hover:bg-gray-50">
<td class="p-4 font-bold text-gray-800">{{ group.name }}</td>
<td class="p-4">{{ group.course.name }}</td>
<td class="p-4 flex items-center gap-2">
<div class="w-6 h-6 rounded-full bg-gray-200 overflow-hidden">
{% if group.teacher.avatar %}
<img src="{{ group.teacher.avatar.url }}" class="w-full h-full object-cover">
{% endif %}
</div>
{{ group.teacher.first_name }}
</td>
<td class="p-4">{{ group.room.name }}</td>
<td class="p-4 text-sm text-gray-500">
{{ group.start_time|time:"H:i" }} - {{ group.end_time|time:"H:i" }}
</td>
<td class="p-4">
<span class="px-2 py-1 text-xs rounded-full font-bold
{% if group.status == 'active' %}bg-green-100 text-green-700
{% elif group.status == 'pending' %}bg-yellow-100 text-yellow-700
{% else %}bg-gray-100 text-gray-700{% endif %}">
{{ group.get_status_display }}
</span>
</td>
</tr>
{% empty %}
<tr><td colspan="6" class="p-6 text-center text-gray-500">Guruhlar mavjud emas.</td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\education\materials.html ---
{% extends 'base.html' %}
{% block title %}Materiallar 📚{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Materiallar 📚</h1>
<p class="text-gray-500 dark:text-gray-400">Video darslar, PDF kitoblar va boshqa o'quv materiallari</p>
</div>
{% if request.user.role in 'super_admin,owner,admin,teacher' %}
<a href="{% url 'material_upload' %}"
class="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl font-medium shadow-lg shadow-primary-500/25 hover:shadow-primary-500/40 transition-all hover:-translate-y-0.5">
<i class="ph ph-upload-simple text-lg"></i>
<span>Yangi Material</span>
</a>
{% endif %}
</div>
<div class="glass-panel p-4 rounded-xl border border-gray-100 dark:border-gray-800">
<form method="GET" class="flex flex-wrap gap-4 items-end">
<div class="flex-1 min-w-[200px]">
<label class="block text-xs font-medium text-gray-500 mb-1">Qidiruv</label>
<input type="text" name="q" value="{{ search }}" placeholder="Nom bo'yicha..."
class="w-full px-4 py-2 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary">
</div>
<div>
<label class="block text-xs font-medium text-gray-500 mb-1">Kategoriya</label>
<select name="category"
class="px-4 py-2 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
{% for cat in categories %}
<option value="{{ cat.id }}" {% if category_id==cat.id|stringformat:"d" %}selected{% endif %}>{{
cat.icon }} {{ cat.name }}</option>
{% endfor %}
</select>
</div>
<div>
<label class="block text-xs font-medium text-gray-500 mb-1">Turi</label>
<select name="type"
class="px-4 py-2 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
<option value="video" {% if material_type=='video' %}selected{% endif %}>🎬 Video</option>
<option value="pdf" {% if material_type=='pdf' %}selected{% endif %}>📄 PDF</option>
<option value="audio" {% if material_type=='audio' %}selected{% endif %}>🎧 Audio</option>
</select>
</div>
<button type="submit"
class="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
<i class="ph ph-magnifying-glass mr-1"></i> Qidirish
</button>
</form>
</div>
{% if featured %}
<div class="mb-6">
<h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
<i class="ph ph-star text-amber-500"></i> Tavsiya etilgan
</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
{% for m in featured %}
<a href="{% url 'material_view' m.pk %}"
class="glass-panel rounded-2xl border-2 border-amber-200 dark:border-amber-900/50 overflow-hidden hover:shadow-xl hover:shadow-amber-500/20 transition-all hover:-translate-y-1 block">
{% if m.thumbnail %}
<img src="{{ m.thumbnail.url }}" alt="{{ m.title }}" class="w-full h-32 object-cover">
{% else %}
<div
class="w-full h-32 bg-gradient-to-br from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/30 flex items-center justify-center">
<span class="text-5xl">{{ m.get_material_type_display|slice:":2" }}</span>
</div>
{% endif %}
<div class="p-4">
<h3 class="font-semibold text-gray-800 dark:text-white truncate">{{ m.title }}</h3>
<div class="flex items-center justify-between mt-2 text-sm text-gray-500">
<span>{{ m.view_count }} ko'rish</span>
<span>{{ m.created_at|date:"d M" }}</span>
</div>
</div>
</a>
{% endfor %}
</div>
</div>
{% endif %}
{% if materials %}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
{% for m in materials %}
<a href="{% url 'material_view' m.pk %}"
class="glass-panel rounded-xl border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow block group">
{% if m.thumbnail %}
<img src="{{ m.thumbnail.url }}" alt="{{ m.title }}"
class="w-full h-28 object-cover group-hover:scale-105 transition-transform duration-300">
{% else %}
<div
class="w-full h-28 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-700 flex items-center justify-center">
<span class="text-4xl">
{% if m.material_type == 'video' %}🎬
{% elif m.material_type == 'pdf' %}📄
{% elif m.material_type == 'audio' %}🎧
{% else %}📦{% endif %}
</span>
</div>
{% endif %}
<div class="p-4">
<div class="flex items-start justify-between gap-2 mb-2">
<h4 class="font-medium text-gray-800 dark:text-white text-sm line-clamp-2">{{ m.title }}</h4>
<span
class="px-2 py-0.5 text-xs rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 whitespace-nowrap">
{{ m.get_material_type_display|slice:"2:" }}
</span>
</div>
<div class="flex items-center justify-between text-xs text-gray-500">
<span><i class="ph ph-eye"></i> {{ m.view_count }}</span>
{% if m.file_size %}
<span>{{ m.file_size }} MB</span>
{% endif %}
</div>
</div>
</a>
{% endfor %}
</div>
{% else %}
<div class="glass-panel p-12 rounded-2xl border border-gray-100 dark:border-gray-800 text-center">
<div class="w-20 h-20 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
<span class="text-4xl">📂</span>
</div>
<h3 class="text-xl font-semibold text-gray-800 dark:text-white mb-2">Materiallar topilmadi</h3>
<p class="text-gray-500">
{% if search %}Qidiruv natijasi bo'sh{% else %}Hozircha materiallar qo'shilmagan{% endif %}
</p>
</div>
{% endif %}
</div>
{% endblock %}

--- templates\education\room_list.html ---
{% extends 'base.html' %}
{% block title %}Xonalar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Xonalar</h1>
<p class="text-gray-500">O'quv markaz xonalari</p>
</div>
<a href="{% url 'room_create' %}"
class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 shadow-sm flex items-center gap-2">
<i class="ph ph-plus"></i> Yangi Xona
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
{% for room in rooms %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition">
<div class="flex items-center gap-4 mb-4">
<div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center text-2xl">
<i class="ph ph-door"></i>
</div>
<div>
<h3 class="font-bold text-gray-800">{{ room.name }}</h3>
<p class="text-xs text-gray-500">{{ room.capacity }} o'rinli</p>
</div>
</div>
<div class="flex items-center justify-between text-sm text-gray-500 border-t pt-4">
<span><i class="ph ph-users-three"></i> Guruhlar: {{ room.groups.count }}</span>
<a href="#" class="text-primary hover:underline">Tahrirlash</a>
</div>
</div>
{% empty %}
<div class="col-span-4 bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
<i class="ph ph-door text-5xl text-gray-300 mb-4"></i>
<h3 class="text-lg font-bold text-gray-800 mb-2">Xonalar topilmadi</h3>
<p class="text-gray-500">Yangi xona qo'shish uchun tugmani bosing</p>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\finance\account_form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="{% url 'finance:account_list' %}" class="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-arrow-left text-xl text-gray-700 dark:text-gray-300"></i>
</a>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">{{ title }}</h1>
</div>
<form method="POST" class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6 space-y-6">
{% csrf_token %}
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Kassa nomi *</label>
{{ form.name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Turi *</label>
{{ form.account_type }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Boshlang'ich Balans</label>
{{ form.balance }}
</div>
<div class="flex justify-end gap-4 pt-4 border-t border-gray-100 dark:border-gray-800">
<a href="{% url 'finance:account_list' %}"
class="px-6 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition">
Bekor qilish
</a>
<button type="submit" class="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition flex items-center gap-2 shadow-lg shadow-primary-500/25">
<i class="ph ph-check"></i> Saqlash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\finance\account_list.html ---
{% extends 'base.html' %}
{% block title %}Kassalar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Kassalar va Hisoblar 💰</h1>
<p class="text-gray-500">Tashkilot kassalari va hisob raqamlari</p>
</div>
<a href="{% url 'finance:account_create' %}"
class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 shadow-sm flex items-center gap-2">
<i class="ph ph-plus"></i> Yangi kassa
</a>
</div>
<div class="bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl p-8 text-white">
<p class="text-green-100 text-sm">Jami balans</p>
<p class="text-4xl font-bold mt-2">{{ total_balance|floatformat:0 }} <span
class="text-xl font-normal text-green-200">UZS</span></p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{% for account in accounts %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition">
<div class="flex items-center justify-between mb-4">
<div class="p-3 rounded-lg
{% if account.account_type == 'cash' %}bg-green-50 text-green-600
{% elif account.account_type == 'bank' %}bg-blue-50 text-blue-600
{% elif account.account_type == 'card' %}bg-purple-50 text-purple-600
{% else %}bg-orange-50 text-orange-600{% endif %}">
{% if account.account_type == 'cash' %}<i class="ph ph-money text-2xl"></i>
{% elif account.account_type == 'bank' %}<i class="ph ph-bank text-2xl"></i>
{% elif account.account_type == 'card' %}<i class="ph ph-credit-card text-2xl"></i>
{% else %}<i class="ph ph-wallet text-2xl"></i>{% endif %}
</div>
<span class="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full font-medium">
{{ account.get_account_type_display }}
</span>
</div>
<h3 class="text-lg font-bold text-gray-800 mb-1">{{ account.name }}</h3>
<p class="text-2xl font-bold {% if account.balance < 0 %}text-red-600{% else %}text-gray-800{% endif %}">
{{ account.balance|floatformat:0 }} <span class="text-sm font-normal text-gray-400">UZS</span>
</p>
</div>
{% empty %}
<div class="col-span-3 bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
<i class="ph ph-vault text-5xl text-gray-300 mb-4"></i>
<h3 class="text-lg font-bold text-gray-800 mb-2">Kassalar topilmadi</h3>
<p class="text-gray-500">Yangi kassa yaratish uchun tugmani bosing</p>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\finance\payroll_calculate.html ---
{% extends 'base.html' %}
{% block title %}Oylik Hisoblash - {{ staff.full_name }}{% endblock %}
{% block header_title %}💰 Oylik Hisoblash{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto space-y-6">
<div class="flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'payroll_list' %}"
class="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-dark-700 transition">
<i class="ph ph-arrow-left text-xl text-gray-600 dark:text-gray-400"></i>
</a>
<div class="flex items-center gap-3">
<div
class="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white text-2xl font-bold">
{{ staff.first_name|first }}
</div>
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">{{ staff.full_name }}</h1>
<p class="text-gray-500">{{ staff.get_role_display }} • {{ selected_month|date:"F Y" }}</p>
</div>
</div>
</div>
</div>
<form method="post" class="space-y-6">
{% csrf_token %}
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div class="glass-panel p-4 rounded-xl text-center">
<p class="text-3xl font-bold text-indigo-600">{{ lessons_count }}</p>
<p class="text-xs text-gray-500 uppercase">O'tilgan Darslar</p>
</div>
<div class="glass-panel p-4 rounded-xl text-center">
<p class="text-3xl font-bold text-yellow-600">{{ late_count }}</p>
<p class="text-xs text-gray-500 uppercase">Kechikishlar</p>
</div>
<div class="glass-panel p-4 rounded-xl text-center">
<p class="text-3xl font-bold text-red-600">{{ absent_count }}</p>
<p class="text-xs text-gray-500 uppercase">Yo'qlamalar</p>
</div>
</div>
<div class="glass-panel p-6 rounded-2xl space-y-6">
<div>
<h3 class="font-semibold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
<i class="ph ph-trend-up text-green-500"></i> Daromadlar
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Asosiy
Oylik</label>
<input type="number" name="base_salary" value="{{ payroll.base_salary|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Darslik
Stavka</label>
<input type="number" name="per_lesson_rate" value="{{ payroll.per_lesson_rate|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">KPI Bonus</label>
<input type="number" name="kpi_bonus" value="{{ payroll.kpi_bonus|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Boshqa
Bonuslar</label>
<input type="number" name="other_bonus" value="{{ payroll.other_bonus|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
</div>
</div>
<hr class="border-gray-200 dark:border-dark-600">
<div>
<h3 class="font-semibold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
<i class="ph ph-trend-down text-red-500"></i> Ushlab Qolishlar
</h3>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Kechikish
Jarimasi</label>
<input type="number" name="late_penalty" value="{{ payroll.late_penalty|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Yo'qlama
Jarimasi</label>
<input type="number" name="absent_penalty" value="{{ payroll.absent_penalty|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Boshqa Ushlab
Qolish</label>
<input type="number" name="other_deductions"
value="{{ payroll.other_deductions|floatformat:0 }}"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">
</div>
</div>
</div>
<hr class="border-gray-200 dark:border-dark-600">
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Izoh</label>
<textarea name="notes" rows="3"
class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white focus:ring-2 focus:ring-indigo-500">{{ payroll.notes }}</textarea>
</div>
</div>
<div class="flex justify-end gap-3">
<a href="{% url 'payroll_list' %}"
class="px-6 py-3 rounded-xl border border-gray-200 dark:border-dark-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700 transition">
Bekor qilish
</a>
<button type="submit"
class="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold hover:shadow-lg hover:shadow-indigo-500/30 transition">
<i class="ph ph-calculator mr-2"></i> Hisoblash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\finance\payroll_list.html ---
{% extends 'base.html' %}
{% block title %}Xodimlar Oyligi{% endblock %}
{% block header_title %}💰 Xodimlar Oyligi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Xodimlar Oyligi</h1>
<p class="text-gray-500 dark:text-gray-400">{{ selected_month|date:"F Y" }} uchun oylik hisobi</p>
</div>
<form method="get" class="flex items-center gap-2">
<select name="month" onchange="this.form.submit()"
class="px-4 py-2 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-gray-200 focus:ring-2 focus:ring-indigo-500">
{% for month in months %}
<option value="{{ month|date:'Y-m' }}" {% if month==selected_month %}selected{% endif %}>
{{ month|date:"F Y" }}
</option>
{% endfor %}
</select>
</form>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
<div class="glass-panel p-5 rounded-2xl">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
<i class="ph ph-money text-2xl text-green-600"></i>
</div>
<div>
<p class="text-2xl font-bold text-gray-800 dark:text-white">{{
stats.total_gross|floatformat:0|default:0 }}</p>
<p class="text-xs text-gray-500 uppercase tracking-wide">Yalpi Summa</p>
</div>
</div>
</div>
<div class="glass-panel p-5 rounded-2xl">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
<i class="ph ph-wallet text-2xl text-blue-600"></i>
</div>
<div>
<p class="text-2xl font-bold text-gray-800 dark:text-white">{{
stats.total_net|floatformat:0|default:0 }}</p>
<p class="text-xs text-gray-500 uppercase tracking-wide">Sof Summa</p>
</div>
</div>
</div>
<div class="glass-panel p-5 rounded-2xl">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
<i class="ph ph-check-circle text-2xl text-purple-600"></i>
</div>
<div>
<p class="text-2xl font-bold text-gray-800 dark:text-white">{{ stats.approved_count }}</p>
<p class="text-xs text-gray-500 uppercase tracking-wide">Tasdiqlangan</p>
</div>
</div>
</div>
<div class="glass-panel p-5 rounded-2xl">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-xl bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center">
<i class="ph ph-clock text-2xl text-orange-600"></i>
</div>
<div>
<p class="text-2xl font-bold text-gray-800 dark:text-white">{{ stats.pending_count }}</p>
<p class="text-xs text-gray-500 uppercase tracking-wide">Kutilmoqda</p>
</div>
</div>
</div>
</div>
<div class="glass-panel rounded-2xl overflow-hidden">
<div class="overflow-x-auto">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-dark-800 text-left">
<tr>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Xodim</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Asosiy</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Bonus</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Ushlab qolish
</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Jami</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Holat</th>
<th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-dark-700">
{% for payroll in payrolls %}
<tr class="hover:bg-gray-50 dark:hover:bg-dark-800 transition">
<td class="px-6 py-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold">
{{ payroll.staff.first_name|first }}
</div>
<div>
<p class="font-semibold text-gray-800 dark:text-white">{{ payroll.staff.full_name }}
</p>
<p class="text-xs text-gray-500">{{ payroll.staff.get_role_display }}</p>
</div>
</div>
</td>
<td class="px-6 py-4 text-gray-700 dark:text-gray-300">{{ payroll.base_salary|floatformat:0 }}
</td>
<td class="px-6 py-4 text-green-600">+{{ payroll.kpi_bonus|floatformat:0 }}</td>
<td class="px-6 py-4 text-red-500">-{{ payroll.total_deductions|floatformat:0 }}</td>
<td class="px-6 py-4 font-bold text-gray-800 dark:text-white">{{
payroll.net_salary|floatformat:0 }}</td>
<td class="px-6 py-4">
<span
class="px-2.5 py-1 text-xs font-bold rounded-lg
{% if payroll.status == 'paid' %}bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400
{% elif payroll.status == 'approved' %}bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400
{% else %}bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400{% endif %}">
{{ payroll.get_status_display }}
</span>
</td>
<td class="px-6 py-4">
<div class="flex items-center gap-2">
<a href="{% url 'calculate_payroll' payroll.staff.id %}?month={{ selected_month|date:'Y-m' }}"
class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 text-gray-600 dark:text-gray-400 transition"
title="Tahrirlash">
<i class="ph ph-pencil"></i>
</a>
{% if payroll.status == 'pending' %}
<form action="{% url 'approve_payroll' payroll.id %}" method="post" class="inline">
{% csrf_token %}
<button type="submit"
class="p-2 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 text-green-600 transition"
title="Tasdiqlash">
<i class="ph ph-check-circle"></i>
</button>
</form>
{% elif payroll.status == 'approved' %}
<a href="{% url 'pay_salary' payroll.id %}"
class="p-2 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 text-blue-600 transition"
title="To'lash">
<i class="ph ph-money"></i>
</a>
{% endif %}
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="7" class="px-6 py-12 text-center text-gray-500">
<i class="ph ph-empty text-4xl mb-2"></i>
<p>Bu oy uchun hisob-kitob yo'q</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% if staff_without_payroll %}
<div class="glass-panel p-6 rounded-2xl">
<h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
<i class="ph ph-plus-circle text-indigo-500"></i> Yangi Hisob-kitob
</h3>
<div class="flex flex-wrap gap-3">
{% for staff in staff_without_payroll %}
<a href="{% url 'calculate_payroll' staff.id %}?month={{ selected_month|date:'Y-m' }}"
class="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-dark-800 border border-gray-200 dark:border-dark-600 rounded-xl hover:shadow-md transition">
<div
class="w-8 h-8 rounded-lg bg-gradient-to-br from-gray-400 to-gray-500 flex items-center justify-center text-white text-sm font-bold">
{{ staff.first_name|first }}
</div>
<span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ staff.full_name }}</span>
</a>
{% endfor %}
</div>
</div>
{% endif %}
</div>
{% endblock %}

--- templates\finance\pending_receipts.html ---
{% extends 'base.html' %}
{% block title %}Tasdiqlanmagan Cheklar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Chek Tasdiqlash 🧾</h1>
<p class="text-gray-500 dark:text-gray-400">Plastik orqali to'lov qilganlarni tekshiring</p>
</div>
<div class="flex gap-3">
<div
class="px-4 py-2 bg-amber-50 dark:bg-amber-900/30 rounded-xl border border-amber-200 dark:border-amber-800">
<span class="text-sm text-amber-600 dark:text-amber-400">Kutilmoqda:</span>
<span class="font-bold text-amber-700 dark:text-amber-300 ml-2">{{ pending_count }}</span>
</div>
<div
class="px-4 py-2 bg-blue-50 dark:bg-blue-900/30 rounded-xl border border-blue-200 dark:border-blue-800">
<span class="text-sm text-blue-600 dark:text-blue-400">Jami summa:</span>
<span class="font-bold text-blue-700 dark:text-blue-300 ml-2">{{ pending_sum|floatformat:0 }}
so'm</span>
</div>
</div>
</div>
{% if pending_receipts %}
<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
{% for tx in pending_receipts %}
<div
class="glass-panel p-6 rounded-2xl border border-gray-100 dark:border-gray-800 hover:shadow-lg transition-all">
<div class="flex items-center gap-4 mb-4">
<div
class="w-12 h-12 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/30">
{{ tx.student.first_name|first|default:"?" }}
</div>
<div class="flex-1">
<h3 class="font-semibold text-gray-800 dark:text-white">
{{ tx.student.first_name }} {{ tx.student.last_name }}
</h3>
<p class="text-sm text-gray-500">{{ tx.student.phone }}</p>
</div>
<span class="px-3 py-1 text-xs font-medium rounded-full
{% if tx.payment_method == 'card' %}bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-400
{% elif tx.payment_method == 'transfer' %}bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400
{% else %}bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400{% endif %}">
{{ tx.get_payment_method_display }}
</span>
</div>
<div class="flex items-center justify-between mb-4 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
<div>
<span class="text-sm text-gray-500">Summa</span>
<p class="text-xl font-bold text-green-600 dark:text-green-400">{{ tx.amount|floatformat:0 }} so'm
</p>
</div>
<div class="text-right">
<span class="text-sm text-gray-500">Sana</span>
<p class="text-sm text-gray-700 dark:text-gray-300">{{ tx.created_at|date:"d M, H:i" }}</p>
</div>
</div>
{% if tx.receipt_image or tx.receipt_file %}
<div class="mb-4">
<span class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
<i class="ph ph-file-image mr-1"></i> Chek:
</span>
{% if tx.receipt_image %}
<a href="{{ tx.receipt_image.url }}" target="_blank"
class="block p-3 bg-gray-100 dark:bg-gray-800 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<img src="{{ tx.receipt_image.url }}" alt="Chek rasmi"
class="w-full h-32 object-cover rounded-lg cursor-zoom-in">
<p class="text-xs text-gray-500 mt-2 text-center">Kattalashtirish uchun bosing</p>
</a>
{% endif %}
{% if tx.receipt_file %}
<a href="{{ tx.receipt_file.url }}" target="_blank"
class="flex items-center gap-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-xl hover:bg-red-100 dark:hover:bg-red-900/30 transition">
<i class="ph ph-file-pdf text-2xl text-red-500"></i>
<span class="text-sm text-red-700 dark:text-red-400">PDF chek - ochish uchun bosing</span>
</a>
{% endif %}
</div>
{% else %}
<div
class="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl">
<p class="text-sm text-yellow-700 dark:text-yellow-400">
<i class="ph ph-warning mr-1"></i> Chek yuklanmagan
</p>
</div>
{% endif %}
{% if tx.description %}
<div class="mb-4 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
<span class="text-xs text-gray-500">Izoh:</span>
<p class="text-sm text-gray-700 dark:text-gray-300">{{ tx.description }}</p>
</div>
{% endif %}
<div class="text-xs text-gray-500 mb-4">
<i class="ph ph-user"></i> Kiritdi: {{ tx.created_by.first_name }}
</div>
<div class="flex gap-3">
<form action="{% url 'finance:verify_receipt' pk=tx.pk %}" method="post" class="flex-1">
{% csrf_token %}
<button type="submit"
class="w-full px-4 py-2.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-medium shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all hover:-translate-y-0.5">
<i class="ph ph-check-circle mr-1"></i> Tasdiqlash
</button>
</form>
<button onclick="openRejectModal({{ tx.pk }})"
class="px-4 py-2.5 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-xl font-medium border border-red-200 dark:border-red-800 hover:bg-red-100 dark:hover:bg-red-900/50 transition-all">
<i class="ph ph-x-circle"></i>
</button>
</div>
</div>
{% endfor %}
</div>
{% else %}
<div class="glass-panel p-12 rounded-2xl border border-gray-100 dark:border-gray-800 text-center">
<div
class="w-20 h-20 mx-auto mb-4 bg-green-100 dark:bg-green-900/40 rounded-full flex items-center justify-center">
<i class="ph ph-check-circle text-4xl text-green-500"></i>
</div>
<h3 class="text-xl font-semibold text-gray-800 dark:text-white mb-2">Hammasi tasdiqlangan! ✅</h3>
<p class="text-gray-500">Tasdiqlanmagan cheklar yo'q</p>
</div>
{% endif %}
</div>
<div id="rejectModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm hidden z-50 flex items-center justify-center">
<div class="bg-white dark:bg-gray-900 rounded-2xl p-6 w-full max-w-md shadow-2xl m-4">
<h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4">
<i class="ph ph-warning text-red-500 mr-2"></i>Chekni rad etish
</h3>
<form id="rejectForm" method="post">
{% csrf_token %}
<div class="mb-4">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Sabab</label>
<textarea name="reason" rows="3"
class="w-full px-4 py-2 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-red-500"
placeholder="Rad etish sababini yozing..."></textarea>
</div>
<div class="flex justify-end gap-3">
<button type="button" onclick="closeRejectModal()"
class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition">
Bekor qilish
</button>
<button type="submit" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
Rad etish
</button>
</div>
</form>
</div>
</div>
<script>
function openRejectModal(pk) {
document.getElementById('rejectModal').classList.remove('hidden');
document.getElementById('rejectForm').action = '{% url "finance:reject_receipt" pk=0 %}'.replace('0', pk);
}
function closeRejectModal() {
document.getElementById('rejectModal').classList.add('hidden');
}
// ESC tugmasi bilan yopish
document.addEventListener('keydown', function (e) {
if (e.key === 'Escape') closeRejectModal();
});
</script>
{% endblock %}

--- templates\finance\report.html ---
{% extends 'base.html' %}
{% block title %}Moliyaviy Hisobot{% endblock %}
{% block content %}
<div class="space-y-8">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Moliyaviy Hisobot 📈</h1>
<p class="text-gray-500">{{ start_date|date:"d M" }} - {{ end_date|date:"d F Y" }}</p>
</div>
<button onclick="window.print()"
class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition flex items-center gap-2">
<i class="ph ph-printer"></i> Chop etish
</button>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="bg-green-50 rounded-xl p-6 border border-green-200">
<p class="text-green-600 text-sm font-medium">Jami Kirim</p>
<p class="text-3xl font-bold text-green-700 mt-2">+{{ total_income|floatformat:0 }}</p>
</div>
<div class="bg-red-50 rounded-xl p-6 border border-red-200">
<p class="text-red-600 text-sm font-medium">Jami Chiqim</p>
<p class="text-3xl font-bold text-red-700 mt-2">-{{ total_expense|floatformat:0 }}</p>
</div>
<div class="bg-blue-50 rounded-xl p-6 border border-blue-200">
<p class="text-blue-600 text-sm font-medium">Sof Foyda</p>
<p class="text-3xl font-bold text-blue-700 mt-2">{{ net_profit|floatformat:0 }}</p>
</div>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 col-span-2">
<h3 class="font-bold text-gray-800 mb-6">30 kunlik dinamika</h3>
<div class="h-64 flex items-end gap-2">
{% for day in daily_stats %}
<div class="flex-1 flex flex-col justify-end h-full gap-1 group relative">
<div
class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-gray-800 text-white text-xs p-2 rounded z-10 whitespace-nowrap">
<p class="font-bold">{{ day.date|date:"d M" }}</p>
<p class="text-green-400">In: {{ day.income }}</p>
<p class="text-red-400">Out: {{ day.expense }}</p>
</div>
{% if day.income > 0 %}
<div class="w-full bg-green-400 rounded-t opacity-80 hover:opacity-100 transition relative"
style="height: {{ day.income|default:1 }}px; max-height: 50%;"></div>
{% endif %}
{% if day.expense > 0 %}
<div class="w-full bg-red-400 rounded-b opacity-80 hover:opacity-100 transition"
style="height: {{ day.expense|default:1 }}px; max-height: 50%;"></div>
{% endif %}
{% if forloop.counter|divisibleby:5 %}
<span class="text-[10px] text-gray-400 text-center mt-2">{{ day.date|date:"d" }}</span>
{% endif %}
</div>
{% endfor %}
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<h3 class="font-bold text-gray-800 mb-4">Kirim Tuzilmasi</h3>
<div class="space-y-4">
{% for cat in income_by_category %}
{% if cat.total > 0 %}
<div>
<div class="flex justify-between text-sm mb-1">
<span class="text-gray-600">{{ cat.name }}</span>
<span class="font-bold text-gray-800">{{ cat.total|floatformat:0 }}</span>
</div>
<div class="w-full bg-gray-100 rounded-full h-2">
<div class="bg-green-500 h-2 rounded-full" style="width: 10%"></div>
</div>
</div>
{% endif %}
{% empty %}
<p class="text-gray-500 text-center">Ma'lumot yo'q</p>
{% endfor %}
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<h3 class="font-bold text-gray-800 mb-4">Chiqim Tuzilmasi</h3>
<div class="space-y-4">
{% for cat in expense_by_category %}
{% if cat.total > 0 %}
<div>
<div class="flex justify-between text-sm mb-1">
<span class="text-gray-600">{{ cat.name }}</span>
<span class="font-bold text-gray-800">{{ cat.total|floatformat:0 }}</span>
</div>
<div class="w-full bg-gray-100 rounded-full h-2">
<div class="bg-red-500 h-2 rounded-full" style="width: 10%"></div>
</div>
</div>
{% endif %}
{% empty %}
<p class="text-gray-500 text-center">Ma'lumot yo'q</p>
{% endfor %}
</div>
</div>
</div>
</div>
{% endblock %}

--- templates\finance\staff_attendance.html ---
{% extends 'base.html' %}
{% block title %}Xodimlar Davomati{% endblock %}
{% block header_title %}📋 HR Davomat{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Xodimlar Davomati</h1>
<p class="text-gray-500">{{ selected_date|date:"d F Y" }}</p>
</div>
<div class="flex gap-2">
<input type="date" value="{{ selected_date|date:'Y-m-d' }}"
onchange="window.location.href='?date=' + this.value"
class="px-4 py-2 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 text-gray-800 dark:text-white">
</div>
</div>
<div class="glass-panel rounded-2xl overflow-hidden">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-dark-800">
<tr>
<th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Xodim</th>
<th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Keldi</th>
<th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Ketdi</th>
<th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Holat</th>
<th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-dark-700">
{% for item in staff_data %}
<tr class="hover:bg-gray-50 dark:hover:bg-dark-800">
<td class="px-6 py-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold">
{{ item.staff.first_name|first }}
</div>
<div>
<p class="font-semibold text-gray-800 dark:text-white">{{ item.staff.full_name }}</p>
<p class="text-xs text-gray-500">{{ item.staff.get_role_display }}</p>
</div>
</div>
</td>
<td class="px-6 py-4 text-gray-700 dark:text-gray-300">
{{ item.check_in|time:"H:i"|default:"-" }}
</td>
<td class="px-6 py-4 text-gray-700 dark:text-gray-300">
{{ item.check_out|time:"H:i"|default:"-" }}
</td>
<td class="px-6 py-4">
<span class="px-2.5 py-1 text-xs font-bold rounded-lg
{% if item.status == 'present' %}bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400
{% elif item.status == 'late' %}bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400
{% elif item.status == 'absent' %}bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400
{% else %}bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400{% endif %}">
{% if item.status == 'present' %}Keldi
{% elif item.status == 'late' %}Kechikdi
{% elif item.status == 'absent' %}Kelmadi
{% else %}Noma'lum{% endif %}
</span>
</td>
<td class="px-6 py-4">
<div class="flex gap-2">
{% if not item.check_in %}
<form action="{% url 'finance:staff_check_in' %}" method="post">
{% csrf_token %}
<input type="hidden" name="staff_id" value="{{ item.staff.id }}">
<button type="submit"
class="px-3 py-1 bg-green-100 text-green-700 rounded-lg text-xs font-medium hover:bg-green-200 transition">
<i class="ph ph-sign-in"></i> Keldi
</button>
</form>
{% elif not item.check_out %}
<form action="{% url 'finance:staff_check_out' %}" method="post">
{% csrf_token %}
<input type="hidden" name="staff_id" value="{{ item.staff.id }}">
<button type="submit"
class="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-medium hover:bg-blue-200 transition">
<i class="ph ph-sign-out"></i> Ketdi
</button>
</form>
{% else %}
<span class="text-gray-400 text-xs">✓ Tugallangan</span>
{% endif %}
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="5" class="px-6 py-12 text-center text-gray-500">
Xodimlar topilmadi
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\finance\student_payments.html ---
{% extends 'base.html' %}
{% block title %}{{ student.first_name }} - To'lovlar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'group_list' %}" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800">{{ student.first_name }} {{ student.last_name }}</h1>
<p class="text-gray-500">To'lovlar tarixi</p>
</div>
</div>
<a href="{% url 'finance:add_student_payment' student.id %}"
class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition flex items-center gap-2">
<i class="ph ph-plus"></i> To'lov qo'shish
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Jami To'lagan</p>
<p class="text-2xl font-bold text-green-600 mt-1">{{ total_paid|floatformat:0 }}</p>
<span class="text-xs text-gray-400">UZS</span>
</div>
<div class="p-3 bg-green-50 rounded-lg text-green-600">
<i class="ph ph-wallet text-2xl"></i>
</div>
</div>
<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
<div>
<p class="text-sm font-medium text-gray-500">Joriy Balans</p>
<p
class="text-2xl font-bold {% if student.balance < 0 %}text-red-600{% else %}text-blue-600{% endif %} mt-1">
{{ student.balance|floatformat:0 }}
</p>
<span class="text-xs text-gray-400">UZS</span>
</div>
<div class="p-3 bg-blue-50 rounded-lg text-blue-600">
<i class="ph ph-coins text-2xl"></i>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<table class="w-full">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4 text-left">Sana</th>
<th class="p-4 text-left">Kategoriya</th>
<th class="p-4 text-left">Kassa</th>
<th class="p-4 text-right">Summa</th>
<th class="p-4 text-center">Holat</th>
<th class="p-4 text-left">Izoh</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for payment in payments %}
<tr class="hover:bg-gray-50 transition">
<td class="p-4 text-gray-600">{{ payment.created_at|date:"d.m.Y H:i" }}</td>
<td class="p-4 font-medium text-gray-800">{{ payment.category.name|default:"-" }}</td>
<td class="p-4 text-gray-600">{{ payment.account.name }}</td>
<td class="p-4 text-right font-bold
{% if payment.transaction_type == 'income' %}text-green-600{% else %}text-red-600{% endif %}">
{% if payment.transaction_type == 'income' %}+{% else %}-{% endif %}{{
payment.amount|floatformat:0 }}
</td>
<td class="p-4 text-center">
<span class="px-2 py-1 text-xs rounded-full font-medium
{% if payment.status == 'confirmed' %}bg-green-100 text-green-700
{% elif payment.status == 'pending' %}bg-yellow-100 text-yellow-700
{% else %}bg-red-100 text-red-700{% endif %}">
{{ payment.get_status_display }}
</span>
</td>
<td class="p-4 text-sm text-gray-500 italic">{{ payment.description }}</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="p-8 text-center text-gray-500">
<i class="ph ph-receipt text-4xl mb-2"></i>
<p>To'lovlar tarixi bo'sh</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\finance\student_payment_form.html ---
{% extends 'base.html' %}
{% block title %}To'lov Qabul Qilish{% endblock %}
{% block content %}
<div class="max-w-xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="{% url 'finance:student_payments' student.id %}"
class="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-arrow-left text-xl text-gray-700 dark:text-gray-300"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">To'lov Qabul Qilish</h1>
<p class="text-gray-500 dark:text-gray-400">{{ student.first_name }} {{ student.last_name }}</p>
</div>
</div>
<form method="POST" enctype="multipart/form-data"
class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6 space-y-6">
{% csrf_token %}
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Kassa *</label>
{{ form.account }}
</div>
<div class="grid grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">To'lov turi *</label>
{{ form.category }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Summa *</label>
{{ form.amount }}
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">To'lov usuli *</label>
{{ form.payment_method }}
<p class="text-xs text-gray-500 mt-1">
<i class="ph ph-info"></i> Plastik yoki bank o'tkazmasi uchun chek yuklash tavsiya etiladi
</p>
</div>
<div id="receiptSection"
class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700">
<h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
<i class="ph ph-receipt mr-1"></i> Chek Yuklash
</h4>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
<label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
<i class="ph ph-image"></i> Rasm (JPG, PNG)
</label>
{{ form.receipt_image }}
</div>
<div>
<label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
<i class="ph ph-file-pdf"></i> PDF Fayl
</label>
{{ form.receipt_file }}
</div>
</div>
<p class="text-xs text-amber-600 dark:text-amber-400 mt-2">
<i class="ph ph-warning"></i> Plastik to'lovlar uchun chek yuklanmasa, admin tekshirishi kerak bo'ladi
</p>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Izoh</label>
{{ form.description }}
</div>
<div class="flex justify-end gap-4 pt-4 border-t border-gray-100 dark:border-gray-800">
<a href="{% url 'finance:student_payments' student.id %}"
class="px-6 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition">
Bekor qilish
</a>
<button type="submit"
class="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg transition flex items-center gap-2 shadow-lg shadow-green-500/25">
<i class="ph ph-check"></i> Qabul qilish
</button>
</div>
</form>
</div>
<script>
function toggleReceiptFields(select) {
const receiptSection = document.getElementById('receiptSection');
if (select.value === 'cash') {
receiptSection.classList.add('hidden');
} else {
receiptSection.classList.remove('hidden');
}
}
// Sahifa yuklanganda tekshirish
document.addEventListener('DOMContentLoaded', function () {
const paymentMethod = document.querySelector('[name="payment_method"]');
if (paymentMethod) {
toggleReceiptFields(paymentMethod);
}
});
</script>
{% endblock %}

--- templates\finance\supply_list.html ---
{% extends 'base.html' %}
{% block title %}Sklad - Sarf Materiallar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
<i class="ph ph-package text-primary-500"></i>
Sklad - Sarf Materiallar
</h1>
<p class="text-gray-500 dark:text-gray-400">Resurslarni kuzatish va boshqarish</p>
</div>
<div class="flex gap-2">
<a href="?low_stock=1"
class="inline-flex items-center gap-2 px-4 py-2.5 {% if show_low_stock %}bg-red-500 text-white{% else %}bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-400{% endif %} rounded-xl font-medium hover:bg-red-600 hover:text-white transition">
<i class="ph ph-warning"></i>
Tugayapti ({{ low_stock_count }})
</a>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div class="glass-panel p-4 rounded-xl border border-blue-100 dark:border-blue-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-blue-100 dark:bg-blue-900/40 rounded-lg">
<i class="ph ph-cube text-xl text-blue-600 dark:text-blue-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Jami Resurslar</p>
<p class="text-xl font-bold text-gray-800 dark:text-white">{{ total_items }}</p>
</div>
</div>
</div>
<div class="glass-panel p-4 rounded-xl border border-orange-100 dark:border-orange-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-orange-100 dark:bg-orange-900/40 rounded-lg">
<i class="ph ph-warning text-xl text-orange-600 dark:text-orange-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Kam Qolganlar</p>
<p class="text-xl font-bold text-orange-600 dark:text-orange-400">{{ low_stock_count }} ta</p>
</div>
</div>
</div>
<div class="glass-panel p-4 rounded-xl border border-green-100 dark:border-green-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-green-100 dark:bg-green-900/40 rounded-lg">
<i class="ph ph-money text-xl text-green-600 dark:text-green-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Umumiy Qiymat</p>
<p class="text-xl font-bold text-green-600 dark:text-green-400">{{ total_value|floatformat:0 }} so'm
</p>
</div>
</div>
</div>
</div>
<div class="glass-panel rounded-xl border border-gray-100 dark:border-gray-800 p-4">
<form method="GET" class="flex flex-wrap items-center gap-4">
<div class="flex-1 min-w-[200px]">
<div class="relative">
<input type="text" name="q" value="{{ current_search|default:'' }}"
placeholder="Material qidirish..." class="w-full pl-10">
<i class="ph ph-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
</div>
</div>
<select name="category" class="min-w-[150px]">
<option value="">Barcha kategoriyalar</option>
{% for cat in categories %}
<option value="{{ cat.id }}" {% if current_category==cat.id|stringformat:"s" %}selected{% endif %}>{{
cat.name }}</option>
{% endfor %}
</select>
<button type="submit"
class="px-4 py-2.5 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 transition">
<i class="ph ph-funnel"></i> Filtrlash
</button>
<a href="{% url 'finance:supply_list' %}"
class="px-4 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-xl font-medium hover:bg-gray-200 transition">
Tozalash
</a>
</form>
</div>
<div class="glass-panel rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
<div class="overflow-x-auto">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-gray-800/50">
<tr>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Material</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Kategoriya</th>
<th class="text-center px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Miqdor</th>
<th class="text-center px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Min</th>
<th class="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Narxi</th>
<th class="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
{% for supply in supplies %}
<tr
class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition {% if supply.is_low_stock %}bg-red-50/50 dark:bg-red-900/10{% endif %}">
<td class="px-6 py-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-lg flex items-center justify-center text-white">
<i class="ph ph-cube text-lg"></i>
</div>
<div>
<div class="font-semibold text-gray-800 dark:text-white">{{ supply.name }}</div>
<div class="text-xs text-gray-500">{{ supply.unit }}</div>
</div>
</div>
</td>
<td class="px-6 py-4">
<span
class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-xs">
{{ supply.category.name|default:"-" }}
</span>
</td>
<td class="px-6 py-4 text-center">
<span
class="text-xl font-bold {% if supply.is_low_stock %}text-red-600 dark:text-red-400{% else %}text-gray-800 dark:text-white{% endif %}">
{{ supply.quantity }}
</span>
{% if supply.is_low_stock %}
<i class="ph ph-warning-circle text-red-500 ml-1"></i>
{% endif %}
</td>
<td class="px-6 py-4 text-center text-gray-500">
{{ supply.min_quantity }}
</td>
<td class="px-6 py-4 text-right text-gray-600 dark:text-gray-400">
{{ supply.unit_price|floatformat:0 }} so'm
</td>
<td class="px-6 py-4">
<div class="flex items-center justify-end gap-2">
<button onclick="openAddModal({{ supply.id }}, '{{ supply.name }}')"
class="p-2 text-white bg-green-500 hover:bg-green-600 rounded-lg transition"
title="Kirim">
<i class="ph ph-plus"></i>
</button>
<button
onclick="openRemoveModal({{ supply.id }}, '{{ supply.name }}', {{ supply.quantity }})"
class="p-2 text-white bg-red-500 hover:bg-red-600 rounded-lg transition"
title="Chiqim">
<i class="ph ph-minus"></i>
</button>
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="px-6 py-12 text-center">
<div class="flex flex-col items-center">
<div
class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
<i class="ph ph-package text-3xl text-gray-400"></i>
</div>
<p class="text-gray-500 dark:text-gray-400">Hozircha materiallar yo'q</p>
</div>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>
<div id="addModal" class="fixed inset-0 bg-black/50 hidden items-center justify-center z-50">
<div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-2xl">
<h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4">📦 Material Kirim</h3>
<form id="addForm" method="POST">
{% csrf_token %}
<p id="addSupplyName" class="text-gray-600 dark:text-gray-400 mb-4"></p>
<div class="mb-4">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Miqdor</label>
<input type="number" name="quantity" required min="1" class="w-full" placeholder="Kiritilgan miqdor">
</div>
<div class="mb-4">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Izoh</label>
<input type="text" name="notes" class="w-full" placeholder="Ixtiyoriy izoh">
</div>
<div class="flex gap-3">
<button type="button" onclick="closeModal('addModal')"
class="flex-1 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-xl font-medium">Bekor</button>
<button type="submit"
class="flex-1 py-2.5 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600">Qo'shish</button>
</div>
</form>
</div>
</div>
<div id="removeModal" class="fixed inset-0 bg-black/50 hidden items-center justify-center z-50">
<div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-2xl">
<h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4">📤 Material Chiqim</h3>
<form id="removeForm" method="POST">
{% csrf_token %}
<p id="removeSupplyName" class="text-gray-600 dark:text-gray-400 mb-2"></p>
<p id="removeSupplyStock" class="text-sm text-gray-500 mb-4"></p>
<div class="mb-4">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Miqdor</label>
<input type="number" name="quantity" id="removeQuantity" required min="1" class="w-full"
placeholder="Yechiladigan miqdor">
</div>
<div class="mb-4">
<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sabab</label>
<input type="text" name="notes" class="w-full" placeholder="Ishlatildi, berildi, yoki boshqa">
</div>
<div class="flex gap-3">
<button type="button" onclick="closeModal('removeModal')"
class="flex-1 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-xl font-medium">Bekor</button>
<button type="submit"
class="flex-1 py-2.5 bg-red-500 text-white rounded-xl font-medium hover:bg-red-600">Yechish</button>
</div>
</form>
</div>
</div>
<script>
function openAddModal(supplyId, supplyName) {
document.getElementById('addSupplyName').textContent = supplyName;
document.getElementById('addForm').action = `/finance/supplies/${supplyId}/add/`;
document.getElementById('addModal').classList.remove('hidden');
document.getElementById('addModal').classList.add('flex');
}
function openRemoveModal(supplyId, supplyName, currentStock) {
document.getElementById('removeSupplyName').textContent = supplyName;
document.getElementById('removeSupplyStock').textContent = `Hozirgi miqdor: ${currentStock}`;
document.getElementById('removeQuantity').max = currentStock;
document.getElementById('removeForm').action = `/finance/supplies/${supplyId}/remove/`;
document.getElementById('removeModal').classList.remove('hidden');
document.getElementById('removeModal').classList.add('flex');
}
function closeModal(modalId) {
document.getElementById(modalId).classList.add('hidden');
document.getElementById(modalId).classList.remove('flex');
}
// ESC bilan yopish
document.addEventListener('keydown', function (e) {
if (e.key === 'Escape') {
closeModal('addModal');
closeModal('removeModal');
}
});
</script>
{% endblock %}

--- templates\finance\transaction_form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-xl mx-auto space-y-6">
<div class="flex items-center gap-4">
<a href="{% url 'finance:transaction_list' %}" class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
</div>
<form method="POST" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
{% csrf_token %}
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Kassa *</label>
{{ form.account }}
</div>
<div class="grid grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Kategoriya *</label>
{{ form.category }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Summa *</label>
{{ form.amount }}
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Izoh</label>
{{ form.description }}
</div>
<div class="flex justify-end gap-4 pt-4 border-t">
<a href="{% url 'finance:transaction_list' %}"
class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
Bekor qilish
</a>
<button type="submit" class="px-6 py-2
{% if type == 'income' %}bg-green-500 hover:bg-green-600{% else %}bg-red-500 hover:bg-red-600{% endif %}
text-white rounded-lg transition flex items-center gap-2">
<i class="ph ph-check"></i> Saqlash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\finance\transaction_list.html ---
{% extends 'base.html' %}
{% block title %}Tranzaksiyalar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Kirim-Chiqim 💸</h1>
<p class="text-gray-500">Barcha moliyaviy operatsiyalar</p>
</div>
<div class="flex items-center gap-2">
<a href="{% url 'finance:add_income' %}"
class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition flex items-center gap-2">
<i class="ph ph-arrow-down"></i> Kirim
</a>
<a href="{% url 'finance:add_expense' %}"
class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition flex items-center gap-2">
<i class="ph ph-arrow-up"></i> Chiqim
</a>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="bg-green-50 border border-green-200 rounded-xl p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-green-600 text-sm">Kirim</p>
<p class="text-2xl font-bold text-green-700 mt-1">+{{ income|floatformat:0 }}</p>
</div>
<i class="ph ph-arrow-down-right text-3xl text-green-400"></i>
</div>
</div>
<div class="bg-red-50 border border-red-200 rounded-xl p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-red-600 text-sm">Chiqim</p>
<p class="text-2xl font-bold text-red-700 mt-1">-{{ expense|floatformat:0 }}</p>
</div>
<i class="ph ph-arrow-up-right text-3xl text-red-400"></i>
</div>
</div>
<div class="bg-blue-50 border border-blue-200 rounded-xl p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-blue-600 text-sm">Balans</p>
<p
class="text-2xl font-bold {% if balance < 0 %}text-red-700{% else %}text-blue-700{% endif %} mt-1">
{{ balance|floatformat:0 }}
</p>
</div>
<i class="ph ph-equals text-3xl text-blue-400"></i>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
<form method="GET" class="flex flex-wrap gap-4 items-end">
<div>
<label class="block text-xs text-gray-500 mb-1">Boshlanish</label>
<input type="date" name="date_from" value="{{ date_from }}"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
</div>
<div>
<label class="block text-xs text-gray-500 mb-1">Tugash</label>
<input type="date" name="date_to" value="{{ date_to }}"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
</div>
<div>
<label class="block text-xs text-gray-500 mb-1">Turi</label>
<select name="type"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
<option value="income" {% if trans_type == 'income' %}selected{% endif %}>Kirim</option>
<option value="expense" {% if trans_type == 'expense' %}selected{% endif %}>Chiqim</option>
</select>
</div>
<div>
<label class="block text-xs text-gray-500 mb-1">Holat</label>
<select name="status"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
<option value="pending" {% if status == 'pending' %}selected{% endif %}>Kutilmoqda</option>
<option value="confirmed" {% if status == 'confirmed' %}selected{% endif %}>Tasdiqlangan</option>
<option value="rejected" {% if status == 'rejected' %}selected{% endif %}>Rad etilgan</option>
</select>
</div>
<button type="submit" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-funnel"></i> Filtrlash
</button>
</form>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<table class="w-full">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4 text-left">Sana</th>
<th class="p-4 text-left">Turi</th>
<th class="p-4 text-left">Kategoriya</th>
<th class="p-4 text-left">Kassa</th>
<th class="p-4 text-left">Bog'liq</th>
<th class="p-4 text-right">Summa</th>
<th class="p-4 text-center">Holat</th>
<th class="p-4 text-right">Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for trans in transactions %}
<tr class="hover:bg-gray-50 transition">
<td class="p-4 text-sm text-gray-600">
{{ trans.created_at|date:"d.m.Y H:i" }}
</td>
<td class="p-4">
{% if trans.transaction_type == 'income' %}
<span class="px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">Kirim</span>
{% else %}
<span class="px-2 py-1 text-xs bg-red-100 text-red-700 rounded-full">Chiqim</span>
{% endif %}
</td>
<td class="p-4 text-sm text-gray-600">{{ trans.category.name|default:"-" }}</td>
<td class="p-4 text-sm text-gray-600">{{ trans.account.name }}</td>
<td class="p-4 text-sm">
{% if trans.student %}
<span class="text-blue-600">{{ trans.student.first_name }}</span>
{% elif trans.staff %}
<span class="text-purple-600">{{ trans.staff.first_name }}</span>
{% else %}
<span class="text-gray-400">-</span>
{% endif %}
</td>
<td class="p-4 text-right font-bold
{% if trans.transaction_type == 'income' %}text-green-600{% else %}text-red-600{% endif %}">
{% if trans.transaction_type == 'income' %}+{% else %}-{% endif %}{{ trans.amount|floatformat:0
}}
</td>
<td class="p-4 text-center">
<span class="px-2 py-1 text-xs rounded-full font-medium
{% if trans.status == 'confirmed' %}bg-green-100 text-green-700
{% elif trans.status == 'pending' %}bg-yellow-100 text-yellow-700
{% else %}bg-red-100 text-red-700{% endif %}">
{{ trans.get_status_display }}
</span>
</td>
<td class="p-4 text-right">
{% if trans.status == 'pending' %}
<div class="flex items-center justify-end gap-2">
<a href="{% url 'finance:confirm_transaction' trans.pk %}"
class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition">
<i class="ph ph-check"></i>
</a>
<a href="{% url 'finance:reject_transaction' trans.pk %}"
class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
<i class="ph ph-x"></i>
</a>
</div>
{% else %}
<span class="text-gray-400 text-xs">{{ trans.confirmed_by.first_name|default:"-" }}</span>
{% endif %}
</td>
</tr>
{% empty %}
<tr>
<td colspan="8" class="p-12 text-center text-gray-500">
<i class="ph ph-receipt text-5xl mb-4"></i>
<p>Tranzaksiyalar topilmadi</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\operations\lesson_list.html ---
{% extends 'base.html' %}
{% block title %}Darslar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">Darslar</h1>
<p class="text-gray-500">Kunlik darslar jadvali va davomat</p>
</div>
<a href="{% url 'operations:schedule' %}"
class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 shadow-sm flex items-center gap-2">
<i class="ph ph-calendar"></i> Haftalik jadval
</a>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
<form method="GET" class="flex flex-wrap gap-4 items-end">
<div>
<label class="block text-xs text-gray-500 mb-1">Sana</label>
<input type="date" name="date" value="{{ date_filter }}"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
</div>
<div>
<label class="block text-xs text-gray-500 mb-1">Guruh</label>
<select name="group"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
{% for group in groups %}
<option value="{{ group.id }}" {% if group_filter==group.id|stringformat:"i" %}selected{% endif %}>
{{ group.name }}
</option>
{% endfor %}
</select>
</div>
<div>
<label class="block text-xs text-gray-500 mb-1">Holat</label>
<select name="status"
class="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
<option value="">Barchasi</option>
<option value="scheduled" {% if status_filter=='scheduled' %}selected{% endif %}>Rejalashtirilgan
</option>
<option value="started" {% if status_filter=='started' %}selected{% endif %}>Darsda</option>
<option value="finished" {% if status_filter=='finished' %}selected{% endif %}>Yakunlangan</option>
</select>
</div>
<button type="submit" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-funnel"></i> Filtrlash
</button>
</form>
</div>
<div class="space-y-4">
{% for lesson in lessons %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition">
<div class="flex items-center gap-4">
<div class="w-20 text-center">
<p class="text-xl font-bold text-gray-800">{{ lesson.start_time|time:"H:i" }}</p>
<p class="text-xs text-gray-500">{{ lesson.end_time|time:"H:i" }}</p>
</div>
<div class="w-1 h-16 rounded-full
{% if lesson.status == 'started' %}bg-blue-500 animate-pulse
{% elif lesson.status == 'finished' %}bg-green-500
{% elif lesson.status == 'cancelled' %}bg-red-500
{% else %}bg-gray-300{% endif %}"></div>
<div class="flex-1">
<h3 class="text-lg font-bold text-gray-800">{{ lesson.group.name }}</h3>
<div class="flex items-center gap-4 text-sm text-gray-500 mt-1">
<span><i class="ph ph-user"></i> {{ lesson.teacher.first_name }}</span>
<span><i class="ph ph-door"></i> {{ lesson.room.name|default:"-" }}</span>
{% if lesson.topic %}
<span><i class="ph ph-book-open"></i> {{ lesson.topic }}</span>
{% endif %}
</div>
</div>
<span class="px-3 py-1 text-xs font-bold rounded-full
{% if lesson.status == 'started' %}text-blue-700 bg-blue-100
{% elif lesson.status == 'finished' %}text-green-700 bg-green-100
{% elif lesson.status == 'cancelled' %}text-red-700 bg-red-100
{% else %}text-gray-600 bg-gray-100{% endif %}">
{{ lesson.get_status_display }}
</span>
<div class="flex items-center gap-2">
{% if lesson.status == 'scheduled' %}
<a href="{% url 'operations:start_lesson' lesson.pk %}"
class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition text-sm flex items-center gap-1">
<i class="ph ph-play"></i> Boshlash
</a>
{% elif lesson.status == 'started' %}
<a href="{% url 'operations:take_attendance' lesson.pk %}"
class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition text-sm flex items-center gap-1">
<i class="ph ph-check-circle"></i> Davomat
</a>
{% else %}
<a href="{% url 'operations:lesson_detail' lesson.pk %}"
class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm flex items-center gap-1">
<i class="ph ph-eye"></i> Ko'rish
</a>
{% endif %}
</div>
</div>
</div>
{% empty %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
<i class="ph ph-calendar-blank text-5xl text-gray-300 mb-4"></i>
<h3 class="text-lg font-bold text-gray-800 mb-2">Darslar topilmadi</h3>
<p class="text-gray-500">Tanlangan sana uchun darslar mavjud emas</p>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\operations\purchase_history.html ---
{% extends 'base.html' %}
{% block title %}Xaridlar Tarixi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'operations:shop' %}"
class="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-arrow-left text-xl text-gray-700 dark:text-gray-300"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Xaridlar Tarixi 📜</h1>
<p class="text-gray-500 dark:text-gray-400">
Jami sarflangan: <span class="font-semibold text-amber-600">{{ total_spent }} 💰</span>
</p>
</div>
</div>
</div>
{% if purchases %}
<div class="space-y-4">
{% for p in purchases %}
<div
class="glass-panel p-4 rounded-xl border border-gray-100 dark:border-gray-800 flex items-center justify-between">
<div class="flex items-center gap-4">
{% if p.item.image %}
<img src="{{ p.item.image.url }}" alt="{{ p.item.name }}" class="w-16 h-16 rounded-lg object-cover">
{% else %}
<div class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
<span class="text-2xl">📦</span>
</div>
{% endif %}
<div>
<h3 class="font-semibold text-gray-800 dark:text-white">{{ p.item.name }}</h3>
<p class="text-sm text-gray-500">{{ p.created_at|date:"d M Y, H:i" }}</p>
{% if request.user.role != 'student' %}
<p class="text-xs text-gray-400">O'quvchi: {{ p.student.first_name }}</p>
{% endif %}
</div>
</div>
<div class="text-right">
<span class="text-lg font-bold text-amber-600 dark:text-amber-400">-{{ p.coin_spent }} 💰</span>
<br>
<span class="px-3 py-1 text-xs font-medium rounded-full
{% if p.status == 'pending' %}bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400
{% elif p.status == 'delivered' %}bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400
{% else %}bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400{% endif %}">
{% if p.status == 'pending' %}Kutilmoqda
{% elif p.status == 'delivered' %}Topshirildi
{% else %}Bekor qilindi{% endif %}
</span>
</div>
</div>
{% endfor %}
</div>
{% else %}
<div class="glass-panel p-12 rounded-2xl border border-gray-100 dark:border-gray-800 text-center">
<div class="w-20 h-20 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
<span class="text-4xl">🛒</span>
</div>
<h3 class="text-xl font-semibold text-gray-800 dark:text-white mb-2">Xaridlar yo'q</h3>
<p class="text-gray-500 mb-4">Siz hali hech narsa sotib olmadingiz</p>
<a href="{% url 'operations:shop' %}"
class="inline-flex items-center gap-2 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition">
<i class="ph ph-storefront"></i> Do'konga o'tish
</a>
</div>
{% endif %}
</div>
{% endblock %}

--- templates\operations\schedule.html ---
{% extends 'base.html' %}
{% block title %}Dars Jadvali{% endblock %}
{% block header_title %}📅 Dars Jadvali{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Haftalik Jadval</h1>
<div class="flex gap-2">
<button
class="px-4 py-2 bg-white dark:bg-dark-800 rounded-xl border border-gray-200 dark:border-dark-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 transition">
<i class="ph ph-caret-left"></i>
</button>
<span class="px-4 py-2 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 rounded-xl font-medium">
Bu hafta
</span>
<button
class="px-4 py-2 bg-white dark:bg-dark-800 rounded-xl border border-gray-200 dark:border-dark-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 transition">
<i class="ph ph-caret-right"></i>
</button>
</div>
</div>
<div class="glass-panel rounded-2xl overflow-hidden">
<div
class="grid grid-cols-7 bg-gray-50 dark:bg-dark-800 text-center text-sm font-semibold text-gray-600 dark:text-gray-400">
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Dushanba</div>
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Seshanba</div>
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Chorshanba</div>
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Payshanba</div>
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Juma</div>
<div class="py-3 border-r border-gray-200 dark:border-dark-600">Shanba</div>
<div class="py-3">Yakshanba</div>
</div>
<div class="grid grid-cols-7 min-h-[400px]">
{% for day in week_days %}
<div class="border-r border-b border-gray-200 dark:border-dark-700 p-2 space-y-1">
{% for lesson in day.lessons %}
<div class="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 border-l-4 border-indigo-500 text-xs">
<p class="font-bold text-indigo-700 dark:text-indigo-300">{{ lesson.group.name }}</p>
<p class="text-gray-500">{{ lesson.start_time|time:"H:i" }} - {{ lesson.end_time|time:"H:i" }}</p>
<p class="text-gray-400">{{ lesson.room.name }}</p>
</div>
{% empty %}
<p class="text-xs text-gray-400 text-center py-4">Dars yo'q</p>
{% endfor %}
</div>
{% endfor %}
</div>
</div>
</div>
{% endblock %}

--- templates\operations\shop.html ---
{% extends 'base.html' %}
{% block title %}Do'kon 🛍️{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Do'kon 🛍️</h1>
<p class="text-gray-500 dark:text-gray-400">Coinlaringizga sovg'alar oling!</p>
</div>
<div class="flex items-center gap-4">
<div
class="px-6 py-3 bg-gradient-to-r from-amber-400 to-orange-500 rounded-2xl shadow-lg shadow-amber-500/30">
<div class="flex items-center gap-3">
<span class="text-3xl">💰</span>
<div>
<span class="text-xs text-amber-100">Sizning balansingiz</span>
<p class="text-2xl font-bold text-white">{{ user_coins }}</p>
</div>
</div>
</div>
<a href="{% url 'operations:purchase_history' %}"
class="px-4 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-clock-counter-clockwise mr-1"></i> Xaridlar tarixi
</a>
</div>
</div>
{% if featured %}
<div class="mb-8">
<h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
<i class="ph ph-star text-amber-500"></i> Tavsiya etilgan
</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
{% for item in featured %}
<div
class="glass-panel rounded-2xl border-2 border-amber-200 dark:border-amber-900/50 overflow-hidden hover:shadow-xl hover:shadow-amber-500/20 transition-all hover:-translate-y-1">
{% if item.image %}
<img src="{{ item.image.url }}" alt="{{ item.name }}" class="w-full h-40 object-cover">
{% else %}
<div
class="w-full h-40 bg-gradient-to-br from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/30 flex items-center justify-center">
<span class="text-6xl">🎁</span>
</div>
{% endif %}
<div class="p-4">
<h3 class="font-semibold text-gray-800 dark:text-white">{{ item.name }}</h3>
<p class="text-sm text-gray-500 truncate">{{ item.description|default:"Premium mahsulot" }}</p>
<div class="flex items-center justify-between mt-3">
<span class="text-lg font-bold text-amber-600 dark:text-amber-400">{{ item.coin_price }}
💰</span>
{% if item.is_in_stock %}
{% if user_coins >= item.coin_price %}
<a href="{% url 'operations:purchase_item' item.id %}"
onclick="return confirm('{{ item.name }} sotib olmoqchimisiz?')"
class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl text-sm font-medium shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition">
Olish
</a>
{% else %}
<span class="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-400 rounded-xl text-sm">
Yetmaydi
</span>
{% endif %}
{% else %}
<span class="px-4 py-2 bg-red-50 dark:bg-red-900/30 text-red-500 rounded-xl text-sm">
Tugagan
</span>
{% endif %}
</div>
</div>
</div>
{% endfor %}
</div>
</div>
{% endif %}
{% for category in categories %}
<div class="mb-8">
<h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
{{ category.icon }} {{ category.name }}
</h2>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
{% for item in items %}
{% if item.category == category %}
<div
class="glass-panel rounded-xl border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow">
{% if item.image %}
<img src="{{ item.image.url }}" alt="{{ item.name }}" class="w-full h-28 object-cover">
{% else %}
<div
class="w-full h-28 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-700 flex items-center justify-center">
<span class="text-4xl">📦</span>
</div>
{% endif %}
<div class="p-3">
<h4 class="font-medium text-gray-800 dark:text-white text-sm truncate">{{ item.name }}</h4>
<div class="flex items-center justify-between mt-2">
<span class="text-sm font-bold text-amber-600 dark:text-amber-400">{{ item.coin_price }}
💰</span>
<span class="text-xs text-gray-400">{{ item.available_stock }} ta</span>
</div>
{% if item.is_in_stock and user_coins >= item.coin_price %}
<a href="{% url 'operations:purchase_item' item.id %}"
onclick="return confirm('{{ item.name }} sotib olmoqchimisiz?')"
class="block w-full mt-2 px-3 py-1.5 bg-green-500 text-white rounded-lg text-xs text-center font-medium hover:bg-green-600 transition">
Sotib olish
</a>
{% elif not item.is_in_stock %}
<span
class="block w-full mt-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 text-gray-400 rounded-lg text-xs text-center">
Tugagan
</span>
{% else %}
<span
class="block w-full mt-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 text-gray-400 rounded-lg text-xs text-center">
Mablag' yetarli emas
</span>
{% endif %}
</div>
</div>
{% endif %}
{% endfor %}
</div>
</div>
{% empty %}
<div class="glass-panel p-12 rounded-2xl border border-gray-100 dark:border-gray-800 text-center">
<div class="w-20 h-20 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
<span class="text-4xl">🛒</span>
</div>
<h3 class="text-xl font-semibold text-gray-800 dark:text-white mb-2">Do'kon bo'sh</h3>
<p class="text-gray-500">Hozircha mahsulotlar qo'shilmagan</p>
</div>
{% endfor %}
{% for item in items %}
{% if not item.category %}
<div class="glass-panel rounded-xl border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-lg transition-shadow"
style="max-width: 200px;">
<div class="p-3">
<h4 class="font-medium text-gray-800 dark:text-white text-sm truncate">{{ item.name }}</h4>
<span class="text-sm font-bold text-amber-600">{{ item.coin_price }} 💰</span>
</div>
</div>
{% endif %}
{% endfor %}
</div>
{% endblock %}

--- templates\operations\shop_admin.html ---
{% extends 'base.html' %}
{% block title %}Do'kon Boshqaruvi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Do'kon Boshqaruvi 🎁</h1>
<p class="text-gray-500 dark:text-gray-400">Mahsulotlar va xaridlarni boshqaring</p>
</div>
<div class="flex gap-3">
{% if pending_count > 0 %}
<div
class="px-4 py-2 bg-amber-50 dark:bg-amber-900/30 rounded-xl border border-amber-200 dark:border-amber-800">
<span class="text-amber-600 dark:text-amber-400">
<i class="ph ph-clock"></i> {{ pending_count }} ta kutilmoqda
</span>
</div>
{% endif %}
<a href="{% url 'operations:shop' %}"
class="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-storefront mr-1"></i> Do'konga o'tish
</a>
</div>
</div>
{% if pending_purchases %}
<div class="glass-panel rounded-2xl border border-amber-200 dark:border-amber-900/50 overflow-hidden">
<div class="p-4 bg-amber-50 dark:bg-amber-900/20 border-b border-amber-200 dark:border-amber-900/50">
<h3 class="font-semibold text-amber-800 dark:text-amber-200">
<i class="ph ph-clock"></i> Topshirilishi kerak ({{ pending_count }})
</h3>
</div>
<div class="divide-y divide-gray-100 dark:divide-gray-800">
{% for p in pending_purchases %}
<div class="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
<div class="flex items-center gap-4">
<div
class="w-12 h-12 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center text-white font-bold">
{{ p.student.first_name|first }}
</div>
<div>
<h4 class="font-semibold text-gray-800 dark:text-white">{{ p.student.first_name }}</h4>
<p class="text-sm text-gray-500">{{ p.item.name }}</p>
<span class="text-xs text-gray-400">{{ p.created_at|date:"d M, H:i" }}</span>
</div>
</div>
<div class="flex items-center gap-3">
<span class="text-amber-600 font-semibold">{{ p.coin_spent }} 💰</span>
<a href="{% url 'operations:deliver_purchase' p.pk %}"
class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
<i class="ph ph-check"></i> Topshirdim
</a>
<a href="{% url 'operations:cancel_purchase' p.pk %}"
onclick="return confirm('Bekor qilsangiz coin qaytariladi')"
class="px-4 py-2 bg-red-50 dark:bg-red-900/30 text-red-600 rounded-lg hover:bg-red-100 transition">
<i class="ph ph-x"></i>
</a>
</div>
</div>
{% endfor %}
</div>
</div>
{% endif %}
<div class="glass-panel rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
<div class="p-4 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
<h3 class="font-semibold text-gray-800 dark:text-white">
<i class="ph ph-package"></i> Mahsulotlar ({{ items.count }})
</h3>
</div>
<div class="overflow-x-auto">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-gray-800/50">
<tr>
<th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Mahsulot</th>
<th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Kategoriya</th>
<th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Narx</th>
<th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Qoldi</th>
<th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Holat</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
{% for item in items %}
<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
<td class="px-4 py-3">
<div class="flex items-center gap-3">
{% if item.image %}
<img src="{{ item.image.url }}" class="w-10 h-10 rounded-lg object-cover">
{% else %}
<div
class="w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
<span class="text-lg">📦</span>
</div>
{% endif %}
<div>
<p class="font-medium text-gray-800 dark:text-white">{{ item.name }}</p>
{% if item.is_featured %}
<span class="text-xs text-amber-500">⭐ Tavsiya</span>
{% endif %}
</div>
</div>
</td>
<td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
{{ item.category.name|default:"-" }}
</td>
<td class="px-4 py-3">
<span class="font-semibold text-amber-600">{{ item.coin_price }} 💰</span>
</td>
<td class="px-4 py-3">
<span
class="{% if item.available_stock < 5 %}text-red-500{% else %}text-gray-600 dark:text-gray-400{% endif %}">
{{ item.available_stock }} ta
</span>
</td>
<td class="px-4 py-3">
{% if item.is_active %}
<span
class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400">
Faol
</span>
{% else %}
<span
class="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
Nofaol
</span>
{% endif %}
</td>
</tr>
{% empty %}
<tr>
<td colspan="5" class="px-4 py-8 text-center text-gray-500">
Mahsulotlar yo'q
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
</div>
{% endblock %}

--- templates\operations\student_ratings.html ---
{% extends 'base.html' %}
{% block title %}O'quvchilar Reytingi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">O'quvchilar Leaderboard 🏆</h1>
<p class="text-gray-500">Eng yaxshi o'quvchilar reytingi</p>
</div>
<a href="{% url 'operations:teacher_ratings' %}"
class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition flex items-center gap-2">
<i class="ph ph-chalkboard-teacher"></i> O'qituvchilar reytingi
</a>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
<table class="w-full">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4 text-center">O'rin</th>
<th class="p-4 text-left">O'quvchi</th>
<th class="p-4 text-center">Guruhlar</th>
<th class="p-4 text-center">Davomat</th>
<th class="p-4 text-center">O'rt. Baho</th>
<th class="p-4 text-center">XP</th>
<th class="p-4 text-center">Umumiy Ball</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for data in students_data %}
<tr class="hover:bg-gray-50 transition
{% if data.rank == 1 %}bg-yellow-50
{% elif data.rank == 2 %}bg-gray-50
{% elif data.rank == 3 %}bg-orange-50{% endif %}">
<td class="p-4 text-center">
{% if data.rank == 1 %}
<span class="text-3xl">🥇</span>
{% elif data.rank == 2 %}
<span class="text-3xl">🥈</span>
{% elif data.rank == 3 %}
<span class="text-3xl">🥉</span>
{% else %}
<span class="text-lg font-bold text-gray-400">#{{ data.rank }}</span>
{% endif %}
</td>
<td class="p-4">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-gradient-to-br
{% if data.rank == 1 %}from-yellow-400 to-orange-500
{% elif data.rank == 2 %}from-gray-300 to-gray-400
{% elif data.rank == 3 %}from-orange-300 to-orange-400
{% else %}from-blue-400 to-indigo-500{% endif %}
text-white flex items-center justify-center font-bold">
{{ data.student.first_name|first }}
</div>
<div>
<p class="font-semibold text-gray-800">{{ data.student.first_name }} {{
data.student.last_name }}</p>
<p class="text-xs text-gray-500">{{ data.student.phone }}</p>
</div>
</div>
</td>
<td class="p-4 text-center">
<span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
{{ data.group_count }}
</span>
</td>
<td class="p-4 text-center">
<div class="flex items-center justify-center gap-2">
<div class="w-16 h-2 bg-gray-100 rounded-full overflow-hidden">
<div class="h-full
{% if data.attendance_rate >= 90 %}bg-green-500
{% elif data.attendance_rate >= 70 %}bg-yellow-500
{% else %}bg-red-500{% endif %} rounded-full"
style="width: {{ data.attendance_rate }}%;"></div>
</div>
<span class="text-sm font-medium text-gray-700">{{ data.attendance_rate }}%</span>
</div>
</td>
<td class="p-4 text-center">
<span class="text-lg font-bold
{% if data.avg_grade >= 80 %}text-green-600
{% elif data.avg_grade >= 60 %}text-yellow-600
{% else %}text-red-600{% endif %}">
{{ data.avg_grade }}
</span>
</td>
<td class="p-4 text-center">
<span
class="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium flex items-center justify-center gap-1">
<i class="ph ph-lightning"></i> {{ data.total_xp }}
</span>
</td>
<td class="p-4 text-center">
<span class="text-xl font-bold text-gray-800">{{ data.score }}</span>
</td>
</tr>
{% empty %}
<tr>
<td colspan="7" class="p-12 text-center text-gray-500">
<i class="ph ph-student text-5xl mb-4"></i>
<p>Hozircha o'quvchilar mavjud emas</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}

--- templates\operations\take_attendance.html ---
{% extends 'base.html' %}
{% block title %}Davomat olish{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'operations:lesson_list' %}"
class="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
<i class="ph ph-arrow-left text-xl"></i>
</a>
<div>
<h1 class="text-2xl font-bold text-gray-800">Davomat olish</h1>
<p class="text-gray-500">{{ lesson.group.name }} - {{ lesson.date|date:"d F Y" }}</p>
</div>
</div>
<div class="flex items-center gap-2">
<span class="px-3 py-1 text-sm rounded-full
{% if lesson.status == 'started' %}text-blue-700 bg-blue-100
{% elif lesson.status == 'finished' %}text-green-700 bg-green-100
{% else %}text-gray-600 bg-gray-100{% endif %}">
{{ lesson.get_status_display }}
</span>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
<div class="flex flex-wrap gap-6 text-sm">
<div class="flex items-center gap-2">
<i class="ph ph-clock text-primary"></i>
<span class="text-gray-600">{{ lesson.start_time|time:"H:i" }} - {{ lesson.end_time|time:"H:i" }}</span>
</div>
<div class="flex items-center gap-2">
<i class="ph ph-user text-primary"></i>
<span class="text-gray-600">{{ lesson.teacher.first_name }} {{ lesson.teacher.last_name }}</span>
</div>
<div class="flex items-center gap-2">
<i class="ph ph-door text-primary"></i>
<span class="text-gray-600">{{ lesson.room.name|default:"Belgilanmagan" }}</span>
</div>
{% if lesson.topic %}
<div class="flex items-center gap-2">
<i class="ph ph-book-open text-primary"></i>
<span class="text-gray-600">{{ lesson.topic }}</span>
</div>
{% endif %}
</div>
</div>
<form method="POST" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
{% csrf_token %}
<div class="p-4 bg-gray-50 border-b flex items-center justify-between">
<h3 class="font-bold text-gray-800">O'quvchilar ro'yxati</h3>
<span class="text-sm text-gray-500">{{ students_data|length }} ta o'quvchi</span>
</div>
<table class="w-full">
<thead class="bg-gray-50 text-gray-600 uppercase text-xs font-semibold">
<tr>
<th class="p-4 text-left">#</th>
<th class="p-4 text-left">O'quvchi</th>
<th class="p-4 text-center">Holat</th>
<th class="p-4 text-center">Baho (0-100)</th>
<th class="p-4 text-left">Izoh</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100">
{% for data in students_data %}
<tr class="hover:bg-gray-50 transition">
<td class="p-4 text-gray-500">{{ forloop.counter }}</td>
<td class="p-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 text-white flex items-center justify-center font-bold">
{{ data.student.first_name|first }}
</div>
<div>
<p class="font-semibold text-gray-800">{{ data.student.first_name }} {{
data.student.last_name }}</p>
<p class="text-xs text-gray-500">{{ data.student.phone }}</p>
</div>
</div>
</td>
<td class="p-4">
<div class="flex items-center justify-center gap-2">
<label class="cursor-pointer">
<input type="radio" name="status_{{ data.student.id }}" value="present" {% if
data.status=='present' %}checked{% endif %} class="sr-only peer">
<span
class="px-3 py-2 rounded-lg border-2 border-gray-200 peer-checked:border-green-500 peer-checked:bg-green-50 peer-checked:text-green-700 transition block text-sm">
✓ Bor
</span>
</label>
<label class="cursor-pointer">
<input type="radio" name="status_{{ data.student.id }}" value="absent" {% if
data.status=='absent' %}checked{% endif %} class="sr-only peer">
<span
class="px-3 py-2 rounded-lg border-2 border-gray-200 peer-checked:border-red-500 peer-checked:bg-red-50 peer-checked:text-red-700 transition block text-sm">
✗ Yo'q
</span>
</label>
<label class="cursor-pointer">
<input type="radio" name="status_{{ data.student.id }}" value="late" {% if
data.status=='late' %}checked{% endif %} class="sr-only peer">
<span
class="px-3 py-2 rounded-lg border-2 border-gray-200 peer-checked:border-yellow-500 peer-checked:bg-yellow-50 peer-checked:text-yellow-700 transition block text-sm">
⏰ Kech
</span>
</label>
<label class="cursor-pointer">
<input type="radio" name="status_{{ data.student.id }}" value="excused" {% if
data.status=='excused' %}checked{% endif %} class="sr-only peer">
<span
class="px-3 py-2 rounded-lg border-2 border-gray-200 peer-checked:border-blue-500 peer-checked:bg-blue-50 peer-checked:text-blue-700 transition block text-sm">
📝 Sababli
</span>
</label>
</div>
</td>
<td class="p-4 text-center">
<input type="number" name="grade_{{ data.student.id }}" value="{{ data.grade|default:'' }}"
min="0" max="100" placeholder="-"
class="w-20 px-3 py-2 text-center rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
</td>
<td class="p-4">
<input type="text" name="comment_{{ data.student.id }}" value="{{ data.comment }}"
placeholder="Izoh..."
class="w-full px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary">
</td>
</tr>
{% empty %}
<tr>
<td colspan="5" class="p-8 text-center text-gray-500">
<i class="ph ph-users text-4xl mb-2"></i>
<p>Bu guruhda o'quvchilar yo'q</p>
</td>
</tr>
{% endfor %}
</tbody>
</table>
<div class="p-4 bg-gray-50 border-t flex items-center justify-between">
<div class="flex items-center gap-4">
<a href="{% url 'operations:finish_lesson' lesson.pk %}"
class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition flex items-center gap-2">
<i class="ph ph-check-circle"></i> Darsni yakunlash
</a>
</div>
<button type="submit"
class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2">
<i class="ph ph-floppy-disk"></i> Saqlash
</button>
</div>
</form>
</div>
{% endblock %}

--- templates\operations\teacher_ratings.html ---
{% extends 'base.html' %}
{% block title %}O'qituvchilar Reytingi{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex items-center justify-between">
<div>
<h1 class="text-2xl font-bold text-gray-800">O'qituvchilar Reytingi 🏆</h1>
<p class="text-gray-500">O'qituvchilar faoliyati va natijalari</p>
</div>
<a href="{% url 'operations:student_ratings' %}"
class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition flex items-center gap-2">
<i class="ph ph-student"></i> O'quvchilar reytingi
</a>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{% for data in teachers_data %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition">
<div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
<div class="flex items-center gap-4">
<div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold">
{{ data.teacher.first_name|first }}
</div>
<div>
<h3 class="text-xl font-bold">{{ data.teacher.first_name }} {{ data.teacher.last_name }}</h3>
<p class="text-indigo-200">{{ data.teacher.phone }}</p>
</div>
</div>
</div>
<div class="grid grid-cols-2 gap-4 p-4">
<div class="text-center p-3 bg-gray-50 rounded-lg">
<p class="text-2xl font-bold text-blue-600">{{ data.group_count }}</p>
<p class="text-xs text-gray-500">Guruh</p>
</div>
<div class="text-center p-3 bg-gray-50 rounded-lg">
<p class="text-2xl font-bold text-green-600">{{ data.student_count }}</p>
<p class="text-xs text-gray-500">O'quvchi</p>
</div>
<div class="text-center p-3 bg-gray-50 rounded-lg">
<p class="text-2xl font-bold text-purple-600">{{ data.lesson_count }}</p>
<p class="text-xs text-gray-500">Dars</p>
</div>
<div class="text-center p-3 bg-gray-50 rounded-lg">
<p class="text-2xl font-bold text-orange-600">{{ data.avg_grade }}</p>
<p class="text-xs text-gray-500">O'rt. Baho</p>
</div>
</div>
<div class="px-4 pb-4">
<div class="flex items-center justify-between text-sm mb-1">
<span class="text-gray-600">Davomat</span>
<span class="font-bold text-gray-800">{{ data.attendance_rate }}%</span>
</div>
<div class="h-2 bg-gray-100 rounded-full overflow-hidden">
<div class="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full transition-all duration-500"
style="width: {{ data.attendance_rate }}%;"></div>
</div>
</div>
</div>
{% empty %}
<div class="col-span-3 bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
<i class="ph ph-chalkboard-teacher text-5xl text-gray-300 mb-4"></i>
<h3 class="text-lg font-bold text-gray-800 mb-2">O'qituvchilar topilmadi</h3>
<p class="text-gray-500">Hozircha o'qituvchilar mavjud emas</p>
</div>
{% endfor %}
</div>
</div>
{% endblock %}

--- templates\registration\login.html ---
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<title>Kirish | Smart Edu</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<script>
tailwind.config = {
theme: {
extend: {
fontFamily: { sans: ['Inter', 'sans-serif'] },
}
}
}
</script>
<style>
body {
background-color: #f3f4f6;
background-image:
radial-gradient(at 0% 0%, hsla(253, 16%, 7%, 1) 0, transparent 50%),
radial-gradient(at 50% 0%, hsla(225, 39%, 30%, 1) 0, transparent 50%),
radial-gradient(at 100% 0%, hsla(339, 49%, 30%, 1) 0, transparent 50%);
background-attachment: fixed;
background-size: cover;
}
.glass-card {
background: rgba(255, 255, 255, 0.7);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.3);
}
</style>
</head>
<body class="flex items-center justify-center h-screen px-4">
<div class="fixed top-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
<div class="fixed bottom-20 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"
style="animation-duration: 4s;"></div>
<div
class="w-full max-w-sm glass-card p-8 rounded-3xl shadow-2xl relative z-10 transition-all hover:scale-[1.01] duration-500">
<div class="text-center mb-8">
<div
class="w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mx-auto flex items-center justify-center text-white text-3xl shadow-lg shadow-blue-500/30 mb-4">
<i class="ph ph-graduation-cap"></i>
</div>
<h1 class="text-2xl font-bold text-gray-800">Smart Edu</h1>
<p class="text-gray-500 text-sm mt-1">Tizimga kirish</p>
</div>
<form method="post" class="space-y-5">
{% csrf_token %}
{% if form.errors %}
<div class="p-3 bg-red-50/80 border border-red-100 text-red-600 text-sm rounded-xl flex items-center gap-2">
<i class="ph ph-warning-circle text-lg"></i>
Login yoki parol noto'g'ri!
</div>
{% endif %}
<div class="space-y-1">
<label class="text-xs font-semibold text-gray-500 uppercase ml-1">Telefon raqam</label>
<div class="relative">
<span class="absolute left-4 top-3.5 text-gray-400 text-lg"><i class="ph ph-phone"></i></span>
<input type="text" name="username" placeholder="998901234567" required
class="w-full pl-11 pr-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:bg-white transition-all placeholder-gray-400 text-gray-800 font-medium">
</div>
</div>
<div class="space-y-1">
<label class="text-xs font-semibold text-gray-500 uppercase ml-1">Parol</label>
<div class="relative">
<span class="absolute left-4 top-3.5 text-gray-400 text-lg"><i class="ph ph-lock-key"></i></span>
<input type="password" name="password" placeholder="••••••••" required
class="w-full pl-11 pr-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:bg-white transition-all placeholder-gray-400 text-gray-800 font-medium">
</div>
</div>
<button type="submit"
class="w-full py-3.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 transition-all transform hover:translate-y-[-2px] active:scale-95 flex items-center justify-center gap-2">
<span>Kirish</span>
<i class="ph ph-arrow-right font-bold"></i>
</button>
</form>
<div class="mt-8 pt-6 border-t border-gray-100/50 text-center">
<a href="#"
class="text-sm text-gray-500 hover:text-blue-600 transition-colors flex items-center justify-center gap-1 group">
<i class="ph ph-question text-lg group-hover:rotate-12 transition-transform"></i>
Yordam kerakmi?
</a>
</div>
</div>
</body>
</html>

--- templates\users\user_confirm_delete.html ---
{% extends 'base.html' %}
{% block content %}
<div class="max-w-md mx-auto mt-10 bg-white p-6 rounded-xl shadow-lg text-center">
<div class="w-16 h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="ph ph-warning text-3xl"></i>
</div>
<h2 class="text-xl font-bold text-gray-800">Rostdan ham o'chirasizmi?</h2>
<p class="text-gray-500 mt-2">Siz <b>{{ user.first_name }} {{ user.last_name }}</b> ni o'chirmoqchisiz. Bu amalni ortga qaytarib bo'lmaydi.</p>
<form method="post" class="mt-6 flex justify-center gap-3">
{% csrf_token %}
<a href="{% url 'user_list' %}" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg">Bekor qilish</a>
<button type="submit" class="px-4 py-2 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700">
Ha, o'chirilsin
</button>
</form>
</div>
{% endblock %}

--- templates\users\user_form.html ---
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto">
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
<h2 class="text-xl font-bold text-gray-800 mb-6">{{ title }}</h2>
{% if form.errors %}
<div class="bg-red-50 text-red-600 p-4 rounded-lg mb-4 text-sm">
{{ form.non_field_errors }}
{% for field in form %}
{% if field.errors %}
<p><b>{{ field.label }}:</b> {{ field.errors|striptags }}</p>
{% endif %}
{% endfor %}
</div>
{% endif %}
<form method="post" enctype="multipart/form-data" class="space-y-4">
{% csrf_token %}
<div class="grid grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Ism</label>
{{ form.first_name }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Familiya</label>
{{ form.last_name }}
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
{{ form.phone }}
</div>
<div class="grid grid-cols-2 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Roli</label>
{{ form.role }}
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Filial</label>
{{ form.branch }}
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Parol (Agar o'zgartirsangiz)</label>
{{ form.password }}
</div>
<div class="flex items-center gap-2 mt-4">
{{ form.is_active }}
<label class="text-sm text-gray-700">Aktiv foydalanuvchi</label>
</div>
<div class="pt-4 flex gap-3">
<button type="submit" class="px-6 py-2 bg-primary text-white font-bold rounded-lg hover:bg-indigo-700">
Saqlash
</button>
<a href="{% url 'user_list' %}" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
Bekor qilish
</a>
</div>
</form>
</div>
</div>
<style>
.form-input, .form-select {
width: 100%;
padding: 0.75rem;
border-radius: 0.5rem;
border: 1px solid #e5e7eb;
background-color: #f9fafb;
}
.form-input:focus, .form-select:focus {
outline: none;
border-color: #4F46E5;
background-color: white;
}
.form-checkbox {
width: 1.2rem;
height: 1.2rem;
color: #4F46E5;
}
</style>
{% endblock %}

--- templates\users\user_list.html ---
{% extends 'base.html' %}
{% block title %}Foydalanuvchilar{% endblock %}
{% block content %}
<div class="space-y-6">
<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
<div>
<h1 class="text-2xl font-bold text-gray-800 dark:text-white">Foydalanuvchilar</h1>
<p class="text-gray-500 dark:text-gray-400">Xodimlar, O'qituvchilar va O'quvchilar</p>
</div>
<div class="flex gap-2">
<a href="?filter=debtors"
class="inline-flex items-center gap-2 px-4 py-2.5 {% if current_filter == 'debtors' %}bg-red-500 text-white{% else %}bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-400{% endif %} rounded-xl font-medium hover:bg-red-600 hover:text-white transition">
<i class="ph ph-warning-circle"></i>
Qarzdorlar ({{ debtors_count }})
</a>
<a href="{% url 'user_create' %}"
class="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-medium shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all hover:-translate-y-0.5">
<i class="ph ph-plus"></i>
Yangi qo'shish
</a>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div class="glass-panel p-4 rounded-xl border border-green-100 dark:border-green-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-green-100 dark:bg-green-900/40 rounded-lg">
<i class="ph ph-student text-xl text-green-600 dark:text-green-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Jami O'quvchilar</p>
<p class="text-xl font-bold text-gray-800 dark:text-white">{{ total_students }}</p>
</div>
</div>
</div>
<div class="glass-panel p-4 rounded-xl border border-orange-100 dark:border-orange-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-orange-100 dark:bg-orange-900/40 rounded-lg">
<i class="ph ph-warning text-xl text-orange-600 dark:text-orange-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Qarzdorlar</p>
<p class="text-xl font-bold text-orange-600 dark:text-orange-400">{{ debtors_count }} nafar</p>
</div>
</div>
</div>
<div class="glass-panel p-4 rounded-xl border border-red-100 dark:border-red-900/30">
<div class="flex items-center gap-3">
<div class="p-3 bg-red-100 dark:bg-red-900/40 rounded-lg">
<i class="ph ph-money text-xl text-red-600 dark:text-red-400"></i>
</div>
<div>
<p class="text-sm text-gray-500 dark:text-gray-400">Umumiy Qarz</p>
<p class="text-xl font-bold text-red-600 dark:text-red-400">{{ total_debt|floatformat:0 }} so'm</p>
</div>
</div>
</div>
</div>
<div class="glass-panel rounded-xl border border-gray-100 dark:border-gray-800 p-4">
<form method="GET" class="flex flex-wrap items-center gap-4">
<div class="flex-1 min-w-[200px]">
<div class="relative">
<input type="text" name="q" value="{{ current_search|default:'' }}"
placeholder="Ism, telefon bo'yicha qidirish..." class="w-full pl-10">
<i class="ph ph-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
</div>
</div>
<select name="role" class="min-w-[150px]">
<option value="">Barcha rollar</option>
{% for value, label in role_choices %}
<option value="{{ value }}" {% if current_role == value %}selected{% endif %}>{{ label }}</option>
{% endfor %}
</select>
<button type="submit"
class="px-4 py-2.5 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 transition">
<i class="ph ph-funnel"></i> Filtrlash
</button>
<a href="{% url 'user_list' %}"
class="px-4 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-xl font-medium hover:bg-gray-200 transition">
Tozalash
</a>
</form>
</div>
<div class="glass-panel rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
<div class="overflow-x-auto">
<table class="w-full">
<thead class="bg-gray-50 dark:bg-gray-800/50">
<tr>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
F.I.O</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Telefon</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Rol
</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Balans</th>
<th class="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Holat</th>
<th class="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
Amallar</th>
</tr>
</thead>
<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
{% for user in users %}
<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
<td class="px-6 py-4">
<div class="flex items-center gap-3">
<div
class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center text-white font-bold overflow-hidden">
{% if user.avatar %}
<img src="{{ user.avatar.url }}" class="w-full h-full object-cover">
{% else %}
{{ user.first_name|first|default:"?" }}
{% endif %}
</div>
<div>
<div class="font-semibold text-gray-800 dark:text-white">{{ user.first_name }} {{
user.last_name }}</div>
<div class="text-xs text-gray-500">ID: {{ user.id }}</div>
</div>
</div>
</td>
<td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ user.phone }}</td>
<td class="px-6 py-4">
<span class="px-2.5 py-1 text-xs rounded-full font-medium
{% if user.role == 'super_admin' %}bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-400
{% elif user.role == 'student' %}bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400
{% elif user.role == 'teacher' %}bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400
{% elif user.role == 'parent' %}bg-pink-100 text-pink-700 dark:bg-pink-900/40 dark:text-pink-400
{% else %}bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400{% endif %}">
{{ user.get_role_display }}
</span>
</td>
<td class="px-6 py-4">
{% if user.role == 'student' %}
<span
class="font-semibold {% if user.balance < 0 %}text-red-600 dark:text-red-400{% else %}text-green-600 dark:text-green-400{% endif %}">
{{ user.balance|floatformat:0 }} so'm
</span>
{% else %}
<span class="text-gray-400">-</span>
{% endif %}
</td>
<td class="px-6 py-4">
{% if user.is_active %}
<span
class="inline-flex items-center gap-1 text-green-600 dark:text-green-400 text-xs font-bold">
<span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Aktiv
</span>
{% else %}
<span class="inline-flex items-center gap-1 text-red-500 text-xs font-bold">
<span class="w-2 h-2 rounded-full bg-red-500"></span> Bloklangan
</span>
{% endif %}
</td>
<td class="px-6 py-4">
<div class="flex items-center justify-end gap-2">
<a href="{% url 'user_update' user.id %}"
class="p-2 text-gray-500 hover:text-blue-600 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/30 transition">
<i class="ph ph-pencil-simple"></i>
</a>
{% if user.role == 'student' %}
<a href="{% url 'finance:student_payment' user.id %}"
class="p-2 text-gray-500 hover:text-green-600 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-green-50 dark:hover:bg-green-900/30 transition"
title="To'lov qabul qilish">
<i class="ph ph-money"></i>
</a>
{% endif %}
<a href="{% url 'user_delete' user.id %}"
class="p-2 text-gray-500 hover:text-red-600 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30 transition">
<i class="ph ph-trash"></i>
</a>
</div>
</td>
</tr>
{% empty %}
<tr>
<td colspan="6" class="px-6 py-12 text-center">
<div class="flex flex-col items-center">
<div
class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
<i class="ph ph-users text-3xl text-gray-400"></i>
</div>
<p class="text-gray-500 dark:text-gray-400">Hech kim topilmadi</p>
<a href="{% url 'user_create' %}" class="text-primary-500 hover:underline mt-2">Yangi
qo'shish →</a>
</div>
</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
{% if users.has_other_pages %}
<div class="px-6 py-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
<div class="text-sm text-gray-500">
{{ users.start_index }} - {{ users.end_index }} / {{ users.paginator.count }} ta
</div>
<div class="flex items-center gap-2">
{% if users.has_previous %}
<a href="?page={{ users.previous_page_number }}{% if current_role %}&role={{ current_role }}{% endif %}{% if current_filter %}&filter={{ current_filter }}{% endif %}{% if current_search %}&q={{ current_search }}{% endif %}"
class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-caret-left"></i>
</a>
{% endif %}
<span
class="px-3 py-1.5 bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-400 rounded-lg text-sm font-medium">
{{ users.number }}
</span>
{% if users.has_next %}
<a href="?page={{ users.next_page_number }}{% if current_role %}&role={{ current_role }}{% endif %}{% if current_filter %}&filter={{ current_filter }}{% endif %}{% if current_search %}&q={{ current_search }}{% endif %}"
class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm hover:bg-gray-200 dark:hover:bg-gray-700 transition">
<i class="ph ph-caret-right"></i>
</a>
{% endif %}
</div>
</div>
{% endif %}
</div>
</div>
{% endblock %}

