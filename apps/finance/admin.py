from django.contrib import admin
from django.utils.html import format_html
from .models import Account, TransactionCategory, Transaction
from .services import confirm_transaction
from django.contrib import messages


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'balance', 'organization')


@admin.register(TransactionCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount_colored', 'transaction_type', 'account', 'student', 'status_colored', 'created_at')
    list_filter = ('status', 'transaction_type', 'account', 'category')
    search_fields = ('student__phone', 'student__first_name', 'description')
    readonly_fields = ('created_by', 'confirmed_by', 'confirmed_at')

    actions = ['approve_transactions']

    def amount_colored(self, obj):
        color = 'green' if obj.transaction_type == 'income' else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{} {:,.0f}</span>', color,
                           "+" if obj.transaction_type == 'income' else "-", obj.amount)

    amount_colored.short_description = "Summa"

    def status_colored(self, obj):
        colors = {'pending': 'orange', 'confirmed': 'green', 'rejected': 'red'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 6px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'), obj.get_status_display())

    status_colored.short_description = "Status"

    # Admin paneldan "Action" orqali tasdiqlash
    def approve_transactions(self, request, queryset):
        count = 0
        for tx in queryset:
            if tx.status == 'pending':
                try:
                    confirm_transaction(tx.id, request.user)
                    count += 1
                except Exception as e:
                    self.message_user(request, f"Xatolik (ID: {tx.id}): {e}", level=messages.ERROR)

        self.message_user(request, f"{count} ta tranzaksiya tasdiqlandi va balanslar yangilandi.")

    approve_transactions.short_description = "Tanlanganlarni tasdiqlash (Balansga o'tkazish)"

    # Avtomatik "Created By" ni qo'shish
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)