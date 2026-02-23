"""
API viewlari.
Umumiy, Ota-ona va O'quvchi endpointlari.
"""
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User, ParentStudent
from apps.education.models import GroupStudent
from apps.operations.models import Lesson, Attendance
from apps.operations.shop import ShopItem
from apps.finance.models import Transaction

from .permissions import IsParent, IsStudent
from .serializers import (
    UserSerializer,
    TransactionSerializer,
    EnrollmentSerializer,
    LessonSerializer,
    AttendanceSerializer,
    ChildAttendanceSerializer,
    PaymentSerializer,
    ChildDetailSerializer,
    ParentDashboardSerializer,
    LeaderboardEntrySerializer,
    StudentStatsSerializer,
    StudentDashboardSerializer,
)


# ============================================
# UMUMIY VIEWLAR (mavjud)
# ============================================

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
            receipt_verified=False,
        )


# ============================================
# OTA-ONA (PARENT) API
# ============================================

def _build_child_data(child):
    """Bitta farzand uchun dashboard ma'lumotlarini yig'adi."""
    from django.db.models import Avg, Count, Q

    enrollments = GroupStudent.objects.filter(
        student=child, status='active',
    ).select_related('group', 'group__course', 'group__teacher', 'group__room')

    stats = Attendance.objects.filter(student=child).aggregate(
        total_att=Count('id'),
        present=Count('id', filter=Q(status='present')),
        avg_grade=Avg('grade'),
        total_xp=Sum('xp_points'),
    )
    total_att = stats['total_att'] or 0
    present = stats['present'] or 0
    att_rate = (present / total_att * 100) if total_att > 0 else 0
    avg_grade = stats['avg_grade'] or 0

    recent_attendance = Attendance.objects.filter(
        student=child,
    ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:5]

    return {
        'child': child,
        'enrollments': enrollments,
        'attendance_rate': round(att_rate, 1),
        'avg_grade': round(float(avg_grade), 1),
        'balance': child.balance,
        'has_debt': child.balance < 0,
        'xp': stats['total_xp'] or 0,
        'recent_attendance': recent_attendance,
    }


class ParentDashboardView(APIView):
    """
    GET /api/parent/dashboard/
    Ota-ona dashboardi - barcha farzandlari haqida umumiy ma'lumot.
    """
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get(self, request):
        parent = request.user
        relations = ParentStudent.objects.filter(
            parent=parent,
        ).select_related('student')

        children = []
        for relation in relations:
            data = _build_child_data(relation.student)
            data['relation_type'] = relation.get_relation_type_display()
            children.append(data)

        total_debt = sum(
            abs(c['balance']) for c in children if c['has_debt']
        )
        has_any_debt = any(c['has_debt'] for c in children)

        serializer = ParentDashboardSerializer({
            'children': children,
            'total_debt': total_debt,
            'has_any_debt': has_any_debt,
        })
        return Response(serializer.data)


class ParentChildrenListView(APIView):
    """
    GET /api/parent/children/
    Ota-onaning barcha farzandlari ro'yxati.
    """
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get(self, request):
        relations = ParentStudent.objects.filter(
            parent=request.user,
        ).select_related('student')

        children = []
        for relation in relations:
            data = _build_child_data(relation.student)
            data['relation_type'] = relation.get_relation_type_display()
            children.append(data)

        serializer = ChildDetailSerializer(children, many=True)
        return Response(serializer.data)


class ParentChildDetailView(APIView):
    """
    GET /api/parent/children/<child_id>/
    Bitta farzand haqida batafsil ma'lumot.
    """
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get(self, request, child_id):
        relation = ParentStudent.objects.filter(
            parent=request.user, student_id=child_id,
        ).select_related('student').first()

        if not relation:
            return Response(
                {'detail': 'Farzand topilmadi.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = _build_child_data(relation.student)
        data['relation_type'] = relation.get_relation_type_display()

        serializer = ChildDetailSerializer(data)
        return Response(serializer.data)


class ParentChildAttendanceView(generics.ListAPIView):
    """
    GET /api/parent/children/<child_id>/attendance/
    Farzandning davomati (sahifalangan).
    """
    serializer_class = ChildAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        child_id = self.kwargs['child_id']
        is_related = ParentStudent.objects.filter(
            parent=self.request.user, student_id=child_id,
        ).exists()
        if not is_related:
            return Attendance.objects.none()
        return Attendance.objects.filter(
            student_id=child_id,
        ).select_related('lesson', 'lesson__group').order_by('-lesson__date')


class ParentChildPaymentsView(generics.ListAPIView):
    """
    GET /api/parent/children/<child_id>/payments/
    Farzandning to'lov tarixi (sahifalangan).
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        child_id = self.kwargs['child_id']
        is_related = ParentStudent.objects.filter(
            parent=self.request.user, student_id=child_id,
        ).exists()
        if not is_related:
            return Transaction.objects.none()
        return Transaction.objects.filter(
            student_id=child_id,
        ).order_by('-created_at')


# ============================================
# O'QUVCHI (STUDENT) API
# ============================================

def _build_student_stats(student):
    """O'quvchi statistikasini hisoblaydi."""
    from django.db.models import Avg, Count, Q

    stats = Attendance.objects.filter(student=student).aggregate(
        total_lessons=Count('id'),
        present_count=Count('id', filter=Q(status='present')),
        avg_grade=Avg('grade'),
        total_xp=Sum('xp_points'),
    )
    total_lessons = stats['total_lessons'] or 0
    present_count = stats['present_count'] or 0
    attendance_rate = (present_count / total_lessons * 100) if total_lessons > 0 else 0
    avg_grade = stats['avg_grade'] or 0
    total_xp = stats['total_xp'] or 0

    coin_balance = total_xp
    if hasattr(student, 'profile_data') and student.profile_data:
        coin_balance = student.profile_data.get('xp', total_xp)

    return {
        'attendance_rate': round(attendance_rate, 1),
        'avg_grade': round(float(avg_grade), 1),
        'total_xp': total_xp,
        'coin_balance': coin_balance,
        'balance': student.balance,
    }


def _build_leaderboard(student):
    """Tashkilot bo'yicha XP reytingi."""
    org = student.organization
    all_ranked = User.objects.filter(
        role='student',
        organization=org,
        is_active=True,
        is_deleted=False,
    ).annotate(
        xp_total=Sum('lesson_attendances__xp_points'),
    ).exclude(xp_total__isnull=True).order_by('-xp_total')

    leaderboard = all_ranked[:10]

    student_rank = 0
    for i, s in enumerate(all_ranked, 1):
        if s.id == student.id:
            student_rank = i
            break

    return leaderboard, student_rank


class StudentDashboardView(APIView):
    """
    GET /api/student/dashboard/
    O'quvchi dashboardi - barcha ma'lumotlar.
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user
        today = timezone.now().date()

        # Guruhlarim
        enrollments = GroupStudent.objects.filter(
            student=student, status='active',
        ).select_related(
            'group', 'group__course', 'group__teacher', 'group__room',
        )
        my_groups = [e.group for e in enrollments]

        # Bugungi darslar
        today_lessons = Lesson.objects.filter(
            group__in=my_groups, date=today,
        ).select_related('group', 'teacher', 'room').order_by('start_time')

        # Keyingi darslar
        upcoming_lessons = Lesson.objects.filter(
            group__in=my_groups, date__gt=today,
        ).select_related('group', 'teacher', 'room').order_by(
            'date', 'start_time',
        )[:10]

        # So'nggi davomat
        recent_attendance = Attendance.objects.filter(
            student=student,
        ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:20]

        # Statistikalar
        stats = _build_student_stats(student)

        # To'lovlar
        payments = Transaction.objects.filter(
            student=student,
        ).order_by('-created_at')[:10]

        # Chart Data (So'nggi 10 ta baho - DB darajasida)
        grade_history = list(
            Attendance.objects.filter(
                student=student, grade__isnull=False,
            ).select_related('lesson').order_by('-lesson__date')[:10]
        )
        grade_history.reverse()
        chart_labels = [att.lesson.date.strftime('%d.%m') for att in grade_history]
        chart_data = [att.grade for att in grade_history]

        # Leaderboard
        leaderboard, student_rank = _build_leaderboard(student)

        # Shop
        org = student.organization
        shop_items_count = 0
        if org:
            shop_items_count = ShopItem.objects.filter(
                organization=org, is_active=True, is_deleted=False,
            ).count()

        serializer = StudentDashboardSerializer({
            'stats': stats,
            'enrollments': enrollments,
            'today_lessons': today_lessons,
            'upcoming_lessons': upcoming_lessons,
            'recent_attendance': recent_attendance,
            'recent_payments': payments,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'leaderboard': leaderboard,
            'student_rank': student_rank,
            'shop_items_count': shop_items_count,
        })
        return Response(serializer.data)


class StudentEnrollmentsView(generics.ListAPIView):
    """
    GET /api/student/enrollments/
    O'quvchining guruhlari.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return GroupStudent.objects.filter(
            student=self.request.user, status='active',
        ).select_related(
            'group', 'group__course', 'group__teacher', 'group__room',
        )


class StudentTodayLessonsView(generics.ListAPIView):
    """
    GET /api/student/lessons/today/
    Bugungi darslar.
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        student = self.request.user
        today = timezone.now().date()
        my_groups = GroupStudent.objects.filter(
            student=student, status='active',
        ).values_list('group_id', flat=True)
        return Lesson.objects.filter(
            group_id__in=my_groups, date=today,
        ).select_related('group', 'teacher', 'room').order_by('start_time')


class StudentUpcomingLessonsView(generics.ListAPIView):
    """
    GET /api/student/lessons/upcoming/
    Kelgusi darslar.
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        student = self.request.user
        today = timezone.now().date()
        my_groups = GroupStudent.objects.filter(
            student=student, status='active',
        ).values_list('group_id', flat=True)
        return Lesson.objects.filter(
            group_id__in=my_groups, date__gt=today,
        ).select_related('group', 'teacher', 'room').order_by(
            'date', 'start_time',
        )[:20]


class StudentAttendanceView(generics.ListAPIView):
    """
    GET /api/student/attendance/
    O'quvchining davomati (sahifalangan).
    """
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Attendance.objects.filter(
            student=self.request.user,
        ).select_related('lesson', 'lesson__group').order_by('-lesson__date')


class StudentPaymentsView(generics.ListAPIView):
    """
    GET /api/student/payments/
    O'quvchining to'lov tarixi (sahifalangan).
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Transaction.objects.filter(
            student=self.request.user,
        ).order_by('-created_at')


class StudentLeaderboardView(APIView):
    """
    GET /api/student/leaderboard/
    XP bo'yicha reyting jadvali.
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        leaderboard, student_rank = _build_leaderboard(request.user)
        serializer = LeaderboardEntrySerializer(leaderboard, many=True)
        return Response({
            'leaderboard': serializer.data,
            'student_rank': student_rank,
        })


class StudentStatsView(APIView):
    """
    GET /api/student/stats/
    O'quvchining statistikasi.
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        stats = _build_student_stats(request.user)
        serializer = StudentStatsSerializer(stats)
        return Response(serializer.data)
