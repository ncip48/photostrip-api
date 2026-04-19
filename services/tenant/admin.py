from django.contrib import admin
from .models import Tenant, TenantUser


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subid",
        "name",
        "is_active",
        "created",
        "updated",
    )

    list_filter = (
        "is_active",
        "created",
        "updated",
    )

    search_fields = (
        "name",
        "subid",
    )

    readonly_fields = (
        "created",
        "updated",
    )

    ordering = ("-created",)


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subid",
        "user",
        "tenant",
        "is_owner",
        "is_active",
        "joined_at",
    )

    list_filter = (
        "is_owner",
        "is_active",
        "joined_at",
    )

    search_fields = (
        "user__email",
        "tenant__name",
        "subid",
    )

    autocomplete_fields = (
        "user",
        "tenant",
    )

    readonly_fields = ("joined_at",)

    ordering = ("-joined_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "tenant")
