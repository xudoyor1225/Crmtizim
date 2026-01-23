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

        # Localhost uchun logic
        if settings.DEBUG and (subdomain == 'localhost' or subdomain == '127'):
            # Agar baza bo'sh bo'lsa, xato bermaslik uchun
            if Organization.objects.exists():
                request.organization = Organization.objects.first()
            else:
                # Avtomatik default tashkilot yaratish (Test uchun)
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
