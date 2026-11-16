from django.contrib import admin
from .models import StudioProfile, Service, ProjectRequest


@admin.register(StudioProfile)
class StudioProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "updated_at")

    def has_add_permission(self, request):
        return not StudioProfile.objects.exists()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    list_editable = ("is_active", "order")


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "status", "created_at")
    list_filter = ("status", "service")
    search_fields = ("name", "email", "description")
    readonly_fields = ("name", "email", "phone", "service", "description", "created_at")
    list_editable = ("status",)
