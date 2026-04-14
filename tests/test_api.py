"""
Parent va Student API endpointlari uchun testlar.
"""
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import User, ParentStudent
from apps.organizations.models import Organization, Branch
from apps.education.models import Course, Group, GroupStudent, Room
from apps.operations.models import Lesson, Attendance
from apps.finance.models import Transaction, Account, TransactionCategory
from apps.hardware.models import FaceIDEvent, FaceIDIntegration, FaceIDUserBinding


class BaseAPITestCase(TestCase):
    """Umumiy test ma'lumotlari."""

    def setUp(self):
        self.org = Organization.objects.create(
            name='Test Markaz', subdomain='test-api',
        )
        self.branch = Branch.objects.create(
            organization=self.org, name='Asosiy filial',
        )

        # Kurs va xona
        self.course = Course.objects.create(
            organization=self.org, name='Ingliz tili',
            price=500000, duration_months=3,
        )
        self.room = Room.objects.create(
            organization=self.org, name='101-xona', capacity=20,
        )

        # O'qituvchi
        self.teacher = User.objects.create_user(
            phone='998901000001', password='test123',
            first_name='Ali', last_name='Valiyev',
            role='teacher', organization=self.org,
        )

        # Guruh
        self.group = Group.objects.create(
            organization=self.org, name='IELTS-A',
            course=self.course, teacher=self.teacher,
            room=self.room, status='active',
            start_date=timezone.now().date() - timedelta(days=30),
        )

        # O'quvchi
        self.student = User.objects.create_user(
            phone='998901000002', password='test123',
            first_name='Jasur', last_name='Karimov',
            role='student', organization=self.org,
            balance=Decimal('-150000'),
        )

        # O'quvchini guruhga qo'shish
        self.enrollment = GroupStudent.objects.create(
            organization=self.org, group=self.group,
            student=self.student, status='active',
        )

        # Dars
        today = timezone.now().date()
        self.lesson = Lesson.objects.create(
            organization=self.org, group=self.group,
            teacher=self.teacher, room=self.room,
            date=today, start_time='10:00', end_time='11:30',
            topic='Unit 1', status='scheduled',
        )

        # Davomat
        self.attendance = Attendance.objects.create(
            organization=self.org, lesson=self.lesson,
            student=self.student, status='present',
            grade=85, xp_points=10,
        )

        # Kassa va tranzaksiya
        self.account = Account.objects.create(
            organization=self.org, name='Naqd kassa',
            account_type='cash', balance=1000000,
        )
        self.category = TransactionCategory.objects.create(
            organization=self.org, name='Kurs tolovi',
            transaction_type='income',
        )

        # Ota-ona
        self.parent = User.objects.create_user(
            phone='998901000003', password='test123',
            first_name='Karim', last_name='Karimov',
            role='parent', organization=self.org,
        )
        self.parent_relation = ParentStudent.objects.create(
            organization=self.org,
            parent=self.parent, student=self.student,
            relation_type='father', is_main_contact=True,
        )
        self.face_integration = FaceIDIntegration.objects.create(
            organization=self.org,
            agent_enabled=True,
        )
        self.face_binding = FaceIDUserBinding.objects.create(
            organization=self.org,
            user=self.student,
            face_id_code='STU-1001',
            sync_enabled=True,
        )

        # Admin (ruxsatsiz kirish testi uchun)
        self.admin_user = User.objects.create_user(
            phone='998901000004', password='test123',
            first_name='Admin', last_name='User',
            role='admin', organization=self.org,
        )

        self.client = APIClient()


# ============================================
# OTA-ONA (PARENT) API TESTLARI
# ============================================

class ParentDashboardAPITest(BaseAPITestCase):
    """Ota-ona dashboard API testlari."""

    def test_parent_dashboard_returns_children(self):
        """Dashboard farzandlar ro'yxatini qaytarishi kerak."""
        FaceIDEvent.objects.create(
            organization=self.org,
            user=self.student,
            face_id_code='STU-1001',
            event_type='CHECK_IN',
            occurred_at=timezone.now().replace(hour=8, minute=55, second=0, microsecond=0),
        )
        self.client.force_authenticate(user=self.parent)
        response = self.client.get('/api/parent/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('children', data)
        self.assertEqual(len(data['children']), 1)
        child = data['children'][0]
        self.assertEqual(child['child']['first_name'], 'Jasur')
        self.assertEqual(child['relation_type'], 'Otasi')
        self.assertTrue(child['has_debt'])
        self.assertIn('today_presence', child)
        self.assertIn('recent_face_logs', child)

    def test_parent_dashboard_debt_calculation(self):
        """Umumiy qarzdorlik to'g'ri hisoblanishi kerak."""
        self.client.force_authenticate(user=self.parent)
        response = self.client.get('/api/parent/dashboard/')
        data = response.json()
        self.assertTrue(data['has_any_debt'])
        self.assertEqual(Decimal(data['total_debt']), Decimal('150000.00'))

    def test_parent_dashboard_unauthenticated(self):
        """Autentifikatsiyasiz kirish mumkin emas."""
        response = self.client.get('/api/parent/dashboard/')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN,
        ])

    def test_parent_dashboard_wrong_role(self):
        """Boshqa roldagi foydalanuvchi kirishi mumkin emas."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/parent/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ParentChildrenAPITest(BaseAPITestCase):
    """Ota-ona farzandlari API testlari."""

    def test_children_list(self):
        """Farzandlar ro'yxati."""
        self.client.force_authenticate(user=self.parent)
        response = self.client.get('/api/parent/children/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_child_detail(self):
        """Bitta farzand tafsilotlari."""
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(f'/api/parent/children/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['child']['id'], self.student.id)
        self.assertIn('enrollments', data)
        self.assertIn('attendance_rate', data)

    def test_child_detail_not_found(self):
        """Boshqa o'quvchining ma'lumotlariga kirish mumkin emas."""
        other_student = User.objects.create_user(
            phone='998901000099', password='test123',
            role='student', organization=self.org,
        )
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(f'/api/parent/children/{other_student.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_child_attendance(self):
        """Farzand davomati."""
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(
            f'/api/parent/children/{self.student.id}/attendance/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)

    def test_child_attendance_unauthorized_child(self):
        """Boshqa o'quvchining davomatiga kirish mumkin emas."""
        other = User.objects.create_user(
            phone='998901000098', password='test123',
            role='student', organization=self.org,
        )
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(
            f'/api/parent/children/{other.id}/attendance/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 0)

    def test_child_payments(self):
        """Farzand to'lovlari."""
        Transaction.objects.create(
            organization=self.org, account=self.account,
            student=self.student, amount=500000,
            transaction_type='income', status='confirmed',
            created_by=self.admin_user, category=self.category,
        )
        self.client.force_authenticate(user=self.parent)
        response = self.client.get(
            f'/api/parent/children/{self.student.id}/payments/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)


# ============================================
# O'QUVCHI (STUDENT) API TESTLARI
# ============================================

class StudentDashboardAPITest(BaseAPITestCase):
    """O'quvchi dashboard API testlari."""

    def test_student_dashboard(self):
        """Dashboard barcha kerakli ma'lumotlarni qaytarishi kerak."""
        today = timezone.localdate()
        FaceIDEvent.objects.create(
            organization=self.org,
            user=self.student,
            face_id_code='STU-1001',
            event_type='CHECK_IN',
            occurred_at=timezone.make_aware(datetime.combine(today, datetime.min.time().replace(hour=8, minute=55))),
        )
        FaceIDEvent.objects.create(
            organization=self.org,
            user=self.student,
            face_id_code='STU-1001',
            event_type='CHECK_OUT',
            occurred_at=timezone.make_aware(datetime.combine(today, datetime.min.time().replace(hour=18, minute=5))),
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('stats', data)
        self.assertIn('enrollments', data)
        self.assertIn('today_lessons', data)
        self.assertIn('upcoming_lessons', data)
        self.assertIn('recent_attendance', data)
        self.assertIn('today_presence', data)
        self.assertIn('recent_face_logs', data)
        self.assertIn('chart_labels', data)
        self.assertIn('chart_data', data)
        self.assertIn('leaderboard', data)
        self.assertIn('student_rank', data)
        self.assertIn('shop_items_count', data)
        self.assertIsNotNone(data['today_presence'])
        self.assertEqual(data['today_presence']['check_in_at'][11:16], '08:55')
        self.assertEqual(data['today_presence']['check_out_at'][11:16], '18:05')

    def test_student_dashboard_stats(self):
        """Statistikalar to'g'ri hisoblanishi kerak."""
        missed_lesson = Lesson.objects.create(
            organization=self.org, group=self.group,
            teacher=self.teacher, room=self.room,
            date=timezone.now().date() - timedelta(days=1),
            start_time='10:00', end_time='11:30',
            topic='Unit 0', status='finished',
        )
        Attendance.objects.create(
            organization=self.org, lesson=missed_lesson,
            student=self.student, status='absent',
            grade=None, xp_points=0,
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/dashboard/')
        data = response.json()
        stats = data['stats']
        self.assertEqual(stats['attendance_rate'], 50.0)
        self.assertEqual(stats['avg_grade'], 85.0)
        self.assertEqual(stats['total_xp'], 10)
        self.assertEqual(Decimal(stats['balance']), Decimal('-150000.00'))
        self.assertEqual(stats['missed_lessons_count'], 1)

    def test_student_dashboard_unauthenticated(self):
        """Autentifikatsiyasiz kirish mumkin emas."""
        response = self.client.get('/api/student/dashboard/')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN,
        ])

    def test_student_dashboard_wrong_role(self):
        """Boshqa roldagi foydalanuvchi kirishi mumkin emas."""
        self.client.force_authenticate(user=self.parent)
        response = self.client.get('/api/student/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentEnrollmentsAPITest(BaseAPITestCase):
    """O'quvchi guruhlari API testlari."""

    def test_enrollments_list(self):
        """O'quvchining guruhlari."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/enrollments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)
        enrollment = data['results'][0]
        self.assertIn('group', enrollment)
        self.assertEqual(enrollment['group']['name'], 'IELTS-A')


class StudentLessonsAPITest(BaseAPITestCase):
    """O'quvchi darslari API testlari."""

    def test_today_lessons(self):
        """Bugungi darslar."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/lessons/today/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)

    def test_upcoming_lessons(self):
        """Kelgusi darslar."""
        # Ertangi dars
        tomorrow = timezone.now().date() + timedelta(days=1)
        Lesson.objects.create(
            organization=self.org, group=self.group,
            teacher=self.teacher, room=self.room,
            date=tomorrow, start_time='10:00', end_time='11:30',
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/lessons/upcoming/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)


class StudentAttendanceAPITest(BaseAPITestCase):
    """O'quvchi davomati API testlari."""

    def test_attendance_list(self):
        """Davomat ro'yxati."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)
        att = data['results'][0]
        self.assertEqual(att['grade'], 85)
        self.assertEqual(att['xp_points'], 10)


class StudentPaymentsAPITest(BaseAPITestCase):
    """O'quvchi to'lovlari API testlari."""

    def test_payments_list(self):
        """To'lovlar tarixi."""
        Transaction.objects.create(
            organization=self.org, account=self.account,
            student=self.student, amount=500000,
            transaction_type='income', status='confirmed',
            created_by=self.admin_user, category=self.category,
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)


class StudentLeaderboardAPITest(BaseAPITestCase):
    """Reyting API testlari."""

    def test_leaderboard(self):
        """Reyting jadvali."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('leaderboard', data)
        self.assertIn('student_rank', data)


class StudentStatsAPITest(BaseAPITestCase):
    """O'quvchi statistikasi API testlari."""

    def test_stats(self):
        """Statistikalar."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/student/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('attendance_rate', data)
        self.assertIn('avg_grade', data)
        self.assertIn('total_xp', data)
        self.assertIn('balance', data)
