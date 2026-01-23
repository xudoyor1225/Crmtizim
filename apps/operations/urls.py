from django.urls import path
from . import views
from . import shop_views

app_name = 'operations'

urlpatterns = [
    # Lessons
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/add/', views.lesson_add, name='lesson_add'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:pk>/start/', views.start_lesson, name='start_lesson'),
    path('lessons/<int:pk>/finish/', views.finish_lesson, name='finish_lesson'),
    path('lessons/<int:pk>/attendance/', views.take_attendance, name='take_attendance'),
    
    # Schedule
    path('schedule/', views.schedule_view, name='schedule'),
    
    # Ratings
    path('ratings/teachers/', views.teacher_ratings, name='teacher_ratings'),
    path('ratings/students/', views.student_ratings, name='student_ratings'),
    
    # Shop (Do'kon)
    path('shop/', shop_views.shop_list, name='shop'),
    path('shop/buy/<int:item_id>/', shop_views.purchase_item, name='purchase_item'),
    path('shop/history/', shop_views.purchase_history, name='purchase_history'),
    path('shop/admin/', shop_views.shop_admin, name='shop_admin'),
    path('shop/deliver/<int:pk>/', shop_views.deliver_purchase, name='deliver_purchase'),
    path('shop/cancel/<int:pk>/', shop_views.cancel_purchase, name='cancel_purchase'),
]
