"""
Resurslar (Inventory) uchun view'lar.
Sarf materiallar va aktivlarni boshqarish.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, F

from apps.finance.inventory import Supply, SupplyCategory, SupplyTransaction, Asset, AssetCategory
from apps.core.audit import log_user_action


@login_required
def supply_list(request):
    """
    Sarf materiallar ro'yxati.
    Low stock alert bilan.
    """
    org = request.user.organization
    
    supplies = Supply.objects.filter(organization=org, is_deleted=False).select_related('category')
    
    # Low stock filter
    show_low_stock = request.GET.get('low_stock')
    if show_low_stock:
        supplies = supplies.filter(quantity__lte=F('min_quantity'))
    
    # Kategoriya filter
    category_id = request.GET.get('category')
    if category_id:
        supplies = supplies.filter(category_id=category_id)
    
    # Qidiruv
    search = request.GET.get('q')
    if search:
        supplies = supplies.filter(name__icontains=search)
    
    # Statistika
    total_items = supplies.count()
    low_stock_count = supplies.filter(quantity__lte=F('min_quantity')).count()
    total_value = supplies.aggregate(
        total=Sum(F('quantity') * F('unit_price'))
    )['total'] or 0
    
    categories = SupplyCategory.objects.filter(organization=org, is_deleted=False)
    
    context = {
        'supplies': supplies,
        'categories': categories,
        'total_items': total_items,
        'low_stock_count': low_stock_count,
        'total_value': total_value,
        'current_category': category_id,
        'current_search': search,
        'show_low_stock': show_low_stock,
    }
    
    return render(request, 'finance/supply_list.html', context)


@login_required
def supply_add_stock(request, supply_id):
    """Sklad: Material qo'shish (kirim)"""
    org = request.user.organization
    supply = get_object_or_404(Supply, pk=supply_id, organization=org)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        
        if quantity > 0:
            SupplyTransaction.objects.create(
                supply=supply,
                transaction_type='in',
                quantity=quantity,
                performed_by=request.user,
                notes=notes,
                organization=org,
            )
            log_user_action(request.user, 'CREATE', 'SupplyTransaction', 
                           None, f"{supply.name}: +{quantity}", request=request)
            messages.success(request, f"{quantity} {supply.unit} qo'shildi!")
        
    return redirect('finance:supply_list')


@login_required  
def supply_remove_stock(request, supply_id):
    """Sklad: Material yechish (chiqim)"""
    org = request.user.organization
    supply = get_object_or_404(Supply, pk=supply_id, organization=org)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        
        if quantity > 0 and quantity <= supply.quantity:
            SupplyTransaction.objects.create(
                supply=supply,
                transaction_type='out',
                quantity=quantity,
                performed_by=request.user,
                notes=notes,
                organization=org,
            )
            log_user_action(request.user, 'CREATE', 'SupplyTransaction', 
                           None, f"{supply.name}: -{quantity}", request=request)
            messages.success(request, f"{quantity} {supply.unit} yechildi!")
        else:
            messages.error(request, "Yetarli miqdor yo'q!")
        
    return redirect('finance:supply_list')


@login_required
def asset_list(request):
    """Aktivlar ro'yxati"""
    org = request.user.organization
    
    assets = Asset.objects.filter(organization=org, is_deleted=False).select_related('category', 'room', 'responsible_person')
    
    # Status filter
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)
    
    # Kategoriya filter  
    category_id = request.GET.get('category')
    if category_id:
        assets = assets.filter(category_id=category_id)
    
    # Statistika
    total_assets = assets.count()
    active_assets = assets.filter(status='active').count()
    total_value = assets.aggregate(total=Sum('purchase_price'))['total'] or 0
    
    categories = AssetCategory.objects.filter(organization=org, is_deleted=False)
    
    context = {
        'assets': assets,
        'categories': categories,
        'total_assets': total_assets,
        'active_assets': active_assets,
        'total_value': total_value,
        'current_status': status,
        'current_category': category_id,
    }
    
    return render(request, 'finance/asset_list.html', context)
