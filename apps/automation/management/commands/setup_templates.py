from django.core.management.base import BaseCommand
from apps.automation.models import NotificationTemplate
from apps.organizations.models import Organization

class Command(BaseCommand):
    help = 'Create default notification templates'

    def handle(self, *args, **options):
        # Hamma tashkilotlar uchun (yoki birinchisi uchun)
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
