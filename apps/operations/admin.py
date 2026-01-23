from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Lesson, Attendance
from .services import finish_lesson_logic


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0  # Bo'sh qatorlar kerak emas
    autocomplete_fields = ['student']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'start_time', 'teacher', 'status')
    list_filter = ('status', 'date', 'group')
    inlines = [AttendanceInline]
    change_list_template = "admin/operations/lesson/change_list.html"  # Custom button uchun

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