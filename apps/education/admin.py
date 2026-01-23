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
    form = GroupForm # Aqlli tekshiruvni ulaymiz
    list_display = ('name', 'course', 'teacher', 'room', 'start_time', 'status')
    list_filter = ('status', 'course', 'teacher')
    inlines = [StudentInline] # Guruh ichida o'quvchi qo'shish
    search_fields = ('name',)

@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'status', 'joined_at')
    list_filter = ('status', 'group')
    search_fields = ('student__phone', 'student__first_name')