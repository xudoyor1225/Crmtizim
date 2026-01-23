from django.contrib import admin
from .models import LeadSource, Stage, Lead, Activity

@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'utm_source')

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_won', 'color')
    list_editable = ('order', 'color') # Ro'yxatni o'zidan tahrirlash

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    readonly_fields = ('created_at',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'source', 'stage', 'assigned_to', 'created_at')
    list_filter = ('stage', 'source', 'assigned_to')
    search_fields = ('full_name', 'phone')
    inlines = [ActivityInline] # Lid ichida tarixni ko'rsatish