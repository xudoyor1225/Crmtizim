import threading
from django.utils.deprecation import MiddlewareMixin
from django.apps import apps
from django.conf import settings
from asgiref.sync import sync_to_async, iscoroutinefunction
import asyncio

_thread_locals = threading.local()

def get_current_organization():
    return getattr(_thread_locals, 'organization', None)


def _get_organization_sync(subdomain):
    """Sinxron tarzda tashkilotni olish"""
    Organization = apps.get_model('organizations', 'Organization')

    # Localhost uchun logic
    if settings.DEBUG and (subdomain == 'localhost' or subdomain == '127'):
        if Organization.objects.exists():
            return Organization.objects.first()
        else:
            # Avtomatik default tashkilot yaratish (Test uchun)
            try:
                from apps.users.models import User
                owner = User.objects.filter(role='super_admin').first()
                if not owner and User.objects.exists():
                    owner = User.objects.first()

                org = Organization.objects.create(
                    name="Smart Edu Test",
                    subdomain="test",
                    owner=owner
                )
                print("⚠️ TEST UCHUN TASHKILOT AVTOMATIK YARATILDI!")
                return org
            except Exception:
                return None
    else:
        try:
            return Organization.objects.get(subdomain=subdomain, is_active=True)
        except Organization.DoesNotExist:
            return None


class TenantMiddleware:
    """
    Multi-tenant middleware - WSGI va ASGI uchun mos.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Async yoki sync ekanligini tekshirish
        self.async_mode = iscoroutinefunction(get_response)

    def __call__(self, request):
        if self.async_mode:
            return self.__acall__(request)
        return self._process_sync(request)

    async def __acall__(self, request):
        """Async versiya"""
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]

        # sync_to_async bilan ORM operatsiyasini bajarish
        request.organization = await sync_to_async(_get_organization_sync)(subdomain)
        _thread_locals.organization = request.organization

        response = await self.get_response(request)
        return response

    def _process_sync(self, request):
        """Sync versiya"""
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]

        request.organization = _get_organization_sync(subdomain)
        _thread_locals.organization = request.organization

        response = self.get_response(request)
        return response


class HTMXMiddleware:
    """
    HTMX middleware - so'rovlarni optimallashtirish uchun.
    HTMX so'rovi bo'lsa, faqat content qismini qaytaradi.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # HTMX so'rov ekanligini belgilash
        request.htmx = request.headers.get('HX-Request') == 'true'
        request.htmx_target = request.headers.get('HX-Target', '')
        request.htmx_trigger = request.headers.get('HX-Trigger', '')

        response = self.get_response(request)

        # HTMX so'rovi uchun qo'shimcha headerlar
        if request.htmx:
            # Sidebar active holatini yangilash uchun
            response['HX-Trigger-After-Swap'] = 'updateSidebar'

            # Login sahifasiga redirect bo'lsa, to'liq sahifa yuklash
            if response.status_code in (301, 302):
                redirect_url = response.get('Location', '')
                login_url = getattr(settings, 'LOGIN_URL', '/login/')
                # LOGIN_URL URL nomi bo'lishi mumkin - resolve qilish
                try:
                    from django.urls import reverse
                    login_path = reverse(login_url)
                except Exception:
                    login_path = login_url
                if login_path and login_path in redirect_url:
                    response['HX-Redirect'] = redirect_url

        return response


