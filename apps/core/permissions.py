"""
Permission decorators va utility funksiyalar.
Role-based access control uchun.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Faqat ma'lum rollarga ruxsat beruvchi decorator.

    Foydalanish:
        @role_required('owner', 'admin')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q!")
                raise PermissionDenied("Bu sahifa faqat admin va owner uchun!")
        return wrapper
    return decorator


def admin_required(view_func):
    """Faqat admin va owner uchun"""
    return role_required('owner', 'admin', 'super_admin')(view_func)


def teacher_required(view_func):
    """O'qituvchi yoki yuqori"""
    return role_required('owner', 'admin', 'teacher')(view_func)


def staff_required(view_func):
    """Har qanday xodim"""
    return role_required('owner', 'admin', 'teacher', 'staff')(view_func)


# REST Framework uchun
from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """REST API: Faqat Owner yoki Admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['owner', 'admin', 'super_admin']


class IsTeacher(BasePermission):
    """REST API: O'qituvchi yoki yuqori"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['owner', 'admin', 'teacher']


class IsStaff(BasePermission):
    """REST API: Har qanday xodim"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['owner', 'admin', 'teacher', 'staff']


class IsSameOrganization(BasePermission):
    """REST API: Bir xil tashkilotdan bo'lishi kerak"""
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'organization'):
            return True
        return request.user.organization == obj.organization
