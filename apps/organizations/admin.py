from django.contrib import admin
from .models import Organization, Branch

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'owner', 'is_active', 'created_at')
    search_fields = ('name', 'subdomain')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'phone', 'is_main')
    list_filter = ('organization',)