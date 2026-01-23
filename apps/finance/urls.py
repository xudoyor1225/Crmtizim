from django.urls import path
from . import views
from . import payroll_views
from . import inventory_views

app_name = 'finance'

urlpatterns = [
    # Accounts (Kassalar)
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_create'),
    path('accounts/<int:pk>/edit/', views.account_edit, name='account_edit'),

    # Categories (Kategoriyalar)
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),

    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/income/', views.add_income, name='add_income'),
    path('transactions/expense/', views.add_expense, name='add_expense'),
    path('transactions/<int:pk>/confirm/', views.confirm_transaction, name='confirm_transaction'),
    path('transactions/<int:pk>/reject/', views.reject_transaction, name='reject_transaction'),
    
    # Student Payments
    path('students/<int:student_id>/payments/', views.student_payments, name='student_payments'),
    path('students/<int:student_id>/payments/add/', views.add_student_payment, name='add_student_payment'),
    path('students/<int:student_id>/payment/', views.add_student_payment, name='student_payment'),  # Alias
    
    # Reports
    path('reports/', views.finance_report, name='report'),
    
    # Payroll (Oylik)
    path('payroll/', payroll_views.payroll_list, name='payroll_list'),
    path('payroll/<int:staff_id>/calculate/', payroll_views.calculate_payroll, name='calculate_payroll'),
    path('payroll/<int:pk>/approve/', payroll_views.approve_payroll, name='approve_payroll'),
    path('payroll/<int:pk>/pay/', payroll_views.pay_salary, name='pay_salary'),
    
    # Staff Attendance (HR)
    path('hr/attendance/', payroll_views.staff_attendance_list, name='staff_attendance_list'),
    path('hr/check-in/', payroll_views.staff_check_in, name='staff_check_in'),
    path('hr/check-out/', payroll_views.staff_check_out, name='staff_check_out'),
    
    # Inventory (Sklad)
    path('supplies/', inventory_views.supply_list, name='supply_list'),
    path('supplies/<int:supply_id>/add/', inventory_views.supply_add_stock, name='supply_add_stock'),
    path('supplies/<int:supply_id>/remove/', inventory_views.supply_remove_stock, name='supply_remove_stock'),
    path('assets/', inventory_views.asset_list, name='asset_list'),
    
    # Receipt Verification (Chek tasdiqlash)
    path('receipts/pending/', views.pending_receipts, name='pending_receipts'),
    path('receipts/<int:pk>/verify/', views.verify_receipt, name='verify_receipt'),
    path('receipts/<int:pk>/reject/', views.reject_receipt, name='reject_receipt'),
]
