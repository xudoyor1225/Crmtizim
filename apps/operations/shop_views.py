"""
Shop views - Do'kon va Xaridlar.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

from apps.operations.shop import ShopCategory, ShopItem, Purchase
from apps.users.models import User
from apps.core.audit import log_user_action


@login_required
def shop_list(request):
    """
    Do'kon sahifasi - O'quvchilar uchun.
    Barcha faol mahsulotlarni ko'rsatadi.
    """
    org = request.organization
    
    # Kategoriyalar bilan mahsulotlar
    categories = ShopCategory.objects.filter(organization=org, is_deleted=False)
    items = ShopItem.objects.filter(
        organization=org, 
        is_deleted=False, 
        is_active=True
    ).select_related('category', 'supply')
    
    # Featured items
    featured = items.filter(is_featured=True)[:4]
    
    # O'quvchi coin balansi
    user_coins = request.user.profile_data.get('xp', 0)
    
    context = {
        'categories': categories,
        'items': items,
        'featured': featured,
        'user_coins': user_coins,
    }
    
    return render(request, 'operations/shop.html', context)


@login_required
def purchase_item(request, item_id):
    """
    Mahsulot sotib olish.
    O'quvchi balansidan coin yechiladi, skladdan mahsulot kamayadi.
    """
    org = request.organization
    item = get_object_or_404(ShopItem, pk=item_id, organization=org, is_active=True)
    
    # Faqat studentlar sotib olishi mumkin
    if request.user.role != 'student':
        messages.error(request, "Faqat o'quvchilar sotib olishi mumkin!")
        return redirect('operations:shop')
    
    # Coin tekshirish
    user_coins = request.user.profile_data.get('xp', 0)
    if user_coins < item.coin_price:
        messages.error(request, f"Yetarli coin yo'q! Sizda: {user_coins} 💰, Kerak: {item.coin_price} 💰")
        return redirect('operations:shop')
    
    # Stock tekshirish
    if not item.is_in_stock:
        messages.error(request, "Bu mahsulot tugagan!")
        return redirect('operations:shop')
    
    # Xarid yaratish
    purchase = Purchase.objects.create(
        organization=org,
        student=request.user,
        item=item,
        quantity=1,
        coin_spent=item.coin_price,
        status='pending'
    )
    
    log_user_action(request.user, 'CREATE', 'Purchase', purchase.id, 
                   f"Do'kondan sotib oldi: {item.name}", request=request)
    
    messages.success(request, f"✅ {item.name} muvaffaqiyatli sotib olindi! Admindan olib keting.")
    return redirect('operations:shop')


@login_required  
def purchase_history(request):
    """
    O'quvchining xaridlar tarixi.
    """
    org = request.organization
    
    if request.user.role == 'student':
        purchases = Purchase.objects.filter(
            organization=org,
            student=request.user,
            is_deleted=False
        ).select_related('item')
    else:
        # Admin / Teacher barcha xaridlarni ko'radi
        purchases = Purchase.objects.filter(
            organization=org,
            is_deleted=False
        ).select_related('item', 'student')
    
    # Statistika
    total_spent = purchases.filter(status__in=['pending', 'delivered']).aggregate(
        total=Sum('coin_spent')
    )['total'] or 0
    
    context = {
        'purchases': purchases[:50],
        'total_spent': total_spent,
    }
    
    return render(request, 'operations/purchase_history.html', context)


# ===========================================
# ADMIN VIEWS
# ===========================================

@login_required
def shop_admin(request):
    """
    Admin uchun do'kon boshqaruvi.
    """
    org = request.organization
    
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('operations:shop')
    
    items = ShopItem.objects.filter(organization=org, is_deleted=False).select_related('category', 'supply')
    categories = ShopCategory.objects.filter(organization=org, is_deleted=False)
    
    # Kutilayotgan xaridlar
    pending_purchases = Purchase.objects.filter(
        organization=org,
        status='pending',
        is_deleted=False
    ).select_related('student', 'item')
    
    context = {
        'items': items,
        'categories': categories,
        'pending_purchases': pending_purchases,
        'pending_count': pending_purchases.count(),
    }
    
    return render(request, 'operations/shop_admin.html', context)


@login_required
def deliver_purchase(request, pk):
    """
    Xaridni topshirish (Admin).
    """
    org = request.organization
    purchase = get_object_or_404(Purchase, pk=pk, organization=org)
    
    if purchase.status == 'pending':
        purchase.status = 'delivered'
        purchase.delivered_by = request.user
        purchase.delivered_at = timezone.now()
        purchase.save()
        
        log_user_action(request.user, 'UPDATE', 'Purchase', purchase.id, 
                       f"Topshirildi: {purchase.item.name}", request=request)
        messages.success(request, f"✅ {purchase.item.name} topshirildi!")
    
    return redirect('operations:shop_admin')


@login_required
def cancel_purchase(request, pk):
    """
    Xaridni bekor qilish va coinni qaytarish.
    """
    org = request.organization
    purchase = get_object_or_404(Purchase, pk=pk, organization=org)
    
    if purchase.status == 'pending':
        # Coinni qaytarish
        xp_data = purchase.student.profile_data.get('xp', 0)
        purchase.student.profile_data['xp'] = xp_data + purchase.coin_spent
        purchase.student.save(update_fields=['profile_data'])
        
        # Stockni qaytarish
        if purchase.item.supply:
            purchase.item.supply.quantity += purchase.quantity
            purchase.item.supply.save()
        else:
            purchase.item.stock += purchase.quantity
            purchase.item.save()
        
        purchase.status = 'cancelled'
        purchase.save()
        
        log_user_action(request.user, 'UPDATE', 'Purchase', purchase.id, 
                       f"Bekor qilindi: {purchase.item.name}", request=request)
        messages.warning(request, f"Xarid bekor qilindi. {purchase.coin_spent} coin qaytarildi.")
    
    return redirect('operations:shop_admin')
