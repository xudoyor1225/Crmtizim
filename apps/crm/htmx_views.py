"""
HTMX Views - Tez partial rendering (ASYNC).
Sahifani to'liq qayta yuklamasdan, faqat kerakli qismini yangilash.
Django 4.1+ async view'larni qo'llab-quvvatlaydi.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.db import models
from asgiref.sync import sync_to_async

from .models import Lead, Stage


@sync_to_async
def get_lead(pk, organization):
    return Lead.objects.select_related('source', 'interested_course', 'stage', 'assigned_to').get(
        pk=pk, organization=organization, is_deleted=False
    )


@sync_to_async
def get_stage(pk, organization):
    return Stage.objects.get(pk=pk, organization=organization, is_deleted=False)


@sync_to_async
def get_leads_for_stage(stage, organization, limit=20):
    return list(Lead.objects.filter(
        stage=stage,
        organization=organization,
        is_deleted=False
    ).select_related('source', 'interested_course').order_by('-created_at')[:limit])


@sync_to_async
def search_leads_db(organization, query, limit=10):
    leads = Lead.objects.filter(
        organization=organization,
        is_deleted=False
    ).select_related('stage', 'source')

    if query:
        leads = leads.filter(
            models.Q(full_name__icontains=query) |
            models.Q(phone__icontains=query)
        )

    return list(leads[:limit])


@sync_to_async
def save_lead(lead, fields):
    lead.save(update_fields=fields)


@login_required
@require_http_methods(["GET"])
async def htmx_lead_card(request, pk):
    """
    Lid kartochkasini HTMX orqali yuklash (ASYNC).
    hx-get="/crm/htmx/lead/1/" hx-target="#lead-1"
    """
    try:
        lead = await get_lead(pk, request.organization)
    except Lead.DoesNotExist:
        return HttpResponse('<div class="text-red-500">Lid topilmadi</div>', status=404)

    html = render_to_string('crm/partials/lead_card.html', {
        'lead': lead,
    }, request=request)

    return HttpResponse(html)


@login_required
@require_http_methods(["GET"])
async def htmx_stage_leads(request, stage_id):
    """
    Bosqichdagi lidlarni HTMX orqali yuklash - lazy loading (ASYNC).
    hx-get="/crm/htmx/stage/1/leads/" hx-trigger="revealed"
    """
    try:
        stage = await get_stage(stage_id, request.organization)
    except Stage.DoesNotExist:
        return HttpResponse('<div class="text-red-500">Bosqich topilmadi</div>', status=404)

    leads = await get_leads_for_stage(stage, request.organization)

    html = render_to_string('crm/partials/stage_leads.html', {
        'leads': leads,
        'stage': stage,
    }, request=request)

    return HttpResponse(html)


@login_required
@require_http_methods(["POST"])
async def htmx_move_lead(request, pk, stage_id):
    """
    Lidni boshqa bosqichga ko'chirish - drag & drop (ASYNC).
    hx-post="/crm/htmx/lead/1/move/2/"
    """
    try:
        lead = await get_lead(pk, request.organization)
        new_stage = await get_stage(stage_id, request.organization)
    except (Lead.DoesNotExist, Stage.DoesNotExist):
        return HttpResponse('<div class="text-red-500">Xatolik</div>', status=404)

    lead.stage = new_stage
    await save_lead(lead, ['stage', 'updated_at'])

    # Yangilangan kartochkani qaytarish
    html = render_to_string('crm/partials/lead_card.html', {
        'lead': lead,
    }, request=request)

    response = HttpResponse(html)
    response['HX-Trigger'] = 'leadMoved'
    return response


@login_required
@require_http_methods(["GET"])
async def htmx_search_leads(request):
    """
    Lidlarni qidirish - debounced input (ASYNC).
    hx-get="/crm/htmx/search/" hx-trigger="keyup changed delay:300ms"
    """
    query = request.GET.get('q', '').strip()

    leads = await search_leads_db(request.organization, query)

    html = render_to_string('crm/partials/search_results.html', {
        'leads': leads,
        'query': query,
    }, request=request)

    return HttpResponse(html)


@login_required
@require_http_methods(["DELETE"])
async def htmx_delete_lead(request, pk):
    """
    Lidni o'chirish - soft delete (ASYNC).
    hx-delete="/crm/htmx/lead/1/" hx-confirm="Ishonchingiz komilmi?"
    """
    try:
        lead = await get_lead(pk, request.organization)
    except Lead.DoesNotExist:
        return HttpResponse('', status=404)

    lead.is_deleted = True
    await save_lead(lead, ['is_deleted', 'updated_at'])

    return HttpResponse('')
