from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.core.audit import log_user_action
from .models import NotificationTemplate
from django import forms

class NotificationTemplateForm(forms.ModelForm):
    class Meta:
        model = NotificationTemplate
        fields = ['title', 'code', 'message_type', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'message_type': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300'}),
            'body': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded-lg border focus:ring-2 border-gray-300', 'rows': 5}),
        }

@login_required
def template_list(request):
    templates = NotificationTemplate.objects.filter(is_deleted=False)
    if request.user.role != 'super_admin' and request.user.organization:
        templates = templates.filter(organization=request.user.organization)
    
    return render(request, 'automation/template_list.html', {'templates': templates})

@login_required
def template_create(request):
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.organization = request.user.organization
            template.save()
            log_user_action(request.user, 'CREATE', 'NotificationTemplate', template.id, str(template), request=request)
            messages.success(request, "Shablon yaratildi!")
            return redirect('automation:template_list')
    else:
        form = NotificationTemplateForm()
    
    return render(request, 'automation/template_form.html', {'form': form, 'title': "Yangi Shablon"})

@login_required
def template_edit(request, pk):
    template = get_object_or_404(NotificationTemplate, pk=pk)
    # Check permissions
    if request.user.role != 'super_admin' and template.organization != request.user.organization:
        messages.error(request, "Ruxsat yo'q!")
        return redirect('automation:template_list')

    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            log_user_action(request.user, 'UPDATE', 'NotificationTemplate', template.id, str(template), request=request)
            messages.success(request, "Shablon yangilandi!")
            return redirect('automation:template_list')
    else:
        form = NotificationTemplateForm(instance=template)
    
    return render(request, 'automation/template_form.html', {'form': form, 'title': "Shablonni tahrirlash"})

@login_required
def template_delete(request, pk):
    template = get_object_or_404(NotificationTemplate, pk=pk)
    if request.method == 'POST':
        template.is_deleted = True
        template.save()
        log_user_action(request.user, 'DELETE', 'NotificationTemplate', template.id, str(template), request=request)
        messages.success(request, "Shablon o'chirildi")
    return redirect('automation:template_list')
