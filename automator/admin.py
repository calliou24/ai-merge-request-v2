from django.contrib import admin
from .models import Template, PAT, Project, MergeRequest


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Customized admin for Template model"""
    list_display = ['name', 'title', 'user', 'created_at', 'is_deleted']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'title')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    def is_deleted(self, obj):
        """Show if soft-deleted"""
        return obj.deleted_at is not None
    is_deleted.boolean = True  # Show as icon
    is_deleted.short_description = 'Deleted'


@admin.register(PAT)
class PATAdmin(admin.ModelAdmin):
    """Customized admin for PAT model"""
    list_display = ['name', 'user', 'is_active','created_at', 'is_deleted']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at', ]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'is_active')
        }),
        ('Token', {
            'fields': ('encrypted_token',),
            'classes': ('collapse',)  # Hide token by default
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_deleted(self, obj):
        return obj.deleted_at is not None
    is_deleted.boolean = True
    is_deleted.short_description = 'Deleted'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Customized admin for Project model"""
    list_display = ['name', 'project_id', 'user', 'created_at', 'is_deleted']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'project_id', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    
    fieldsets = (
        ('Project Info', {
            'fields': ('user', 'name', 'project_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_deleted(self, obj):
        return obj.deleted_at is not None
    is_deleted.boolean = True
    is_deleted.short_description = 'Deleted'


@admin.register(MergeRequest)
class MergeRequestAdmin(admin.ModelAdmin):
    """Customized admin for MergeRequest model"""
    list_display = ['merge_request_id', 'title_short', 'user', 'project', 'created_at', 'is_deleted']
    list_filter = ['created_at', 'user', 'project']
    search_fields = ['merge_request_id', 'title', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at', 'project_name']
    
    fieldsets = (
        ('Merge Request Info', {
            'fields': ('user', 'project', 'merge_request_id')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('project_name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_short(self, obj):
        """Show shortened title"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'Title'
    
    def is_deleted(self, obj):
        return obj.deleted_at is not None
    is_deleted.boolean = True
    is_deleted.short_description = 'Deleted'
