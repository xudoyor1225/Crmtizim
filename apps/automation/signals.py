from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.operations.models import Attendance
from apps.finance.models import Transaction
from apps.automation.services import send_notification

@receiver(post_save, sender=Attendance)
def attendance_notification(sender, instance, created, **kwargs):
    """
    Davomat o'zgarganda (agar 'absent' bo'lsa) ota-onaga xabar yuborish.
    """
    if instance.status == 'absent':
        # Ota-onani topamiz
        student = instance.student
        
        # O'quvchining barcha ota-onalari (yoki asosiysi)
        parents = student.parent_relations.all()
        
        for relation in parents:
            parent = relation.parent
            
            # Xabar yuborish
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
    """
    To'lov tasdiqlanganda o'quvchi va ota-onaga xabar yuborish.
    """
    if instance.transaction_type == 'income' and instance.status == 'confirmed':
        student = instance.student
        if not student:
            return

        # O'quvchiga xabar
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
        
        # Ota-onasiga ham xabar (agar bo'lsa)
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
