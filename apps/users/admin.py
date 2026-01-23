from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ParentStudent


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Username maydonini admin paneldan olib tashlaymiz
    ordering = ('phone',)
    list_display = ('phone', 'first_name', 'last_name', 'role', 'organization', 'balance')
    list_filter = ('role', 'organization', 'is_active')
    search_fields = ('phone', 'first_name', 'last_name')

    # Fieldsetlarni (formani) to'g'irlash
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