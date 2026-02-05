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


# =============================================
# SUPPLY CRUD (Sklad materiallari)
# =============================================

@login_required
def supply_create(request):
    """Yangi material qo'shish"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    categories = SupplyCategory.objects.filter(organization=org, is_deleted=False)

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        unit = request.POST.get('unit', 'dona')
        quantity = int(request.POST.get('quantity', 0) or 0)
        min_quantity = int(request.POST.get('min_quantity', 5) or 5)
        unit_price = float(request.POST.get('unit_price', 0) or 0)
        description = request.POST.get('description', '')

        if name:
            supply = Supply.objects.create(
                organization=org,
                name=name,
                category_id=category_id if category_id else None,
                unit=unit,
                quantity=quantity,
                min_quantity=min_quantity,
                unit_price=unit_price,
                description=description
            )
            log_user_action(request.user, 'CREATE', 'Supply', supply.id,
                           f"Material yaratildi: {name}", request=request)
            messages.success(request, f"'{name}' muvaffaqiyatli qo'shildi!")
            return redirect('finance:supply_list')

    return render(request, 'finance/supply_form.html', {
        'title': 'Yangi material',
        'categories': categories
    })


@login_required
def supply_edit(request, pk):
    """Materialni tahrirlash"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    supply = get_object_or_404(Supply, pk=pk, organization=org)
    categories = SupplyCategory.objects.filter(organization=org, is_deleted=False)

    if request.method == 'POST':
        supply.name = request.POST.get('name', supply.name)
        category_id = request.POST.get('category')
        supply.category_id = category_id if category_id else None
        supply.unit = request.POST.get('unit', supply.unit)
        supply.quantity = int(request.POST.get('quantity', 0) or 0)
        supply.min_quantity = int(request.POST.get('min_quantity', 5) or 5)
        supply.unit_price = float(request.POST.get('unit_price', 0) or 0)
        supply.description = request.POST.get('description', '')
        supply.save()

        log_user_action(request.user, 'UPDATE', 'Supply', supply.id,
                       f"Material yangilandi: {supply.name}", request=request)
        messages.success(request, "Material yangilandi!")
        return redirect('finance:supply_list')

    return render(request, 'finance/supply_form.html', {
        'title': 'Materialni tahrirlash',
        'supply': supply,
        'categories': categories
    })


@login_required
def supply_delete(request, pk):
    """Materialni o'chirish"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    supply = get_object_or_404(Supply, pk=pk, organization=org)

    log_user_action(request.user, 'DELETE', 'Supply', supply.id,
                   f"Material o'chirildi: {supply.name}", request=request)
    supply.is_deleted = True
    supply.save()
    messages.warning(request, f"'{supply.name}' o'chirildi!")
    return redirect('finance:supply_list')


# =============================================
# SUPPLY CATEGORY CRUD
# =============================================

@login_required
def supply_category_list(request):
    """Sklad kategoriyalari"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    categories = SupplyCategory.objects.filter(organization=org, is_deleted=False)

    return render(request, 'finance/supply_category_list.html', {'categories': categories})


@login_required
def supply_category_create(request):
    """Yangi kategoriya"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            SupplyCategory.objects.create(organization=org, name=name)
            messages.success(request, f"'{name}' kategoriyasi yaratildi!")
            return redirect('finance:supply_category_list')

    return render(request, 'finance/supply_category_form.html', {'title': 'Yangi kategoriya'})


@login_required
def supply_category_edit(request, pk):
    """Kategoriyani tahrirlash"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    category = get_object_or_404(SupplyCategory, pk=pk, organization=org)

    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.save()
        messages.success(request, "Kategoriya yangilandi!")
        return redirect('finance:supply_category_list')

    return render(request, 'finance/supply_category_form.html', {
        'title': 'Kategoriyani tahrirlash',
        'category': category
    })


@login_required
def supply_category_delete(request, pk):
    """Kategoriyani o'chirish"""
    if request.user.role not in ['super_admin', 'owner', 'admin']:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('finance:supply_list')

    org = request.user.organization
    category = get_object_or_404(SupplyCategory, pk=pk, organization=org)
    category.is_deleted = True
    category.save()
    messages.warning(request, f"'{category.name}' o'chirildi!")
    return redirect('finance:supply_category_list')

