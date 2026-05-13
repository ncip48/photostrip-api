# subscription/admin.py

from django.contrib import admin

from .models import (
    Subscription,
    SubscriptionInvoice,
    SubscriptionPlan,
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "price",
        "currency",
        "billing_interval",
        "is_active",
        "created",
    )
    list_filter = (
        "billing_interval",
        "is_active",
        "created",
    )
    search_fields = (
        "name",
        "code",
        "description",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    prepopulated_fields = {
        "code": ("name",),
    }
    ordering = (
        "price",
        "id",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "plan",
        "status",
        "current_period_start",
        "current_period_end",
        "is_active",
    )

    search_fields = (
        "tenant__name",
        "plan__name",
        "plan__code",
    )

    autocomplete_fields = (
        "tenant",
        "plan",
    )

    list_filter = (
        "status",
        "plan",
    )

    ordering = ("-created",)

    fieldsets = (
        (
            "Subscription Info",
            {
                "fields": (
                    "tenant",
                    "plan",
                    "status",
                )
            },
        ),
        (
            "Period",
            {
                "fields": (
                    "current_period_start",
                    "current_period_end",
                    "trial_start",
                    "trial_end",
                )
            },
        ),
        (
            "Cancellation",
            {
                "fields": (
                    "cancel_at_period_end",
                    "cancelled_at",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        fields = ["created", "updated"]

        if obj:
            fields += ["is_active", "is_trial"]

        return fields


@admin.register(SubscriptionInvoice)
class SubscriptionInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "tenant",
        "subscription",
        "amount",
        "currency",
        "status",
        "payment_method",
        "issued_at",
        "due_at",
        "paid_at",
    )
    list_filter = (
        "status",
        "payment_method",
        "currency",
        "issued_at",
    )
    search_fields = (
        "invoice_number",
        "tenant__name",
        "payment_reference",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    autocomplete_fields = (
        "tenant",
        "subscription",
    )
    ordering = ("-issued_at",)

    fieldsets = (
        (
            "Invoice Info",
            {
                "fields": (
                    "tenant",
                    "subscription",
                    "invoice_number",
                    "status",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "amount",
                    "currency",
                    "payment_method",
                    "payment_reference",
                    "paid_at",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "issued_at",
                    "due_at",
                )
            },
        ),
        (
            "Additional",
            {
                "fields": (
                    "notes",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )