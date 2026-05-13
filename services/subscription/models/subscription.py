from __future__ import annotations

import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionQuerySet",
    "SubscriptionManager",
    "Subscription",
)


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(
            status=Subscription.SubscriptionStatus.ACTIVE,
            current_period_start__lte=now,
            current_period_end__gte=now,
        )

    def for_tenant(self, tenant):
        return self.filter(tenant=tenant)


_SubscriptionManagerBase = models.Manager.from_queryset(SubscriptionQuerySet)


class SubscriptionManager(_SubscriptionManagerBase):
    pass


class Subscription(get_subid_model()):
    """
    Active subscription owned by a tenant/company.
    """

    class SubscriptionStatus(models.TextChoices):
        TRIALING = "trialing", _("Trialing")
        ACTIVE = "active", _("Active")
        PAST_DUE = "past_due", _("Past Due")
        CANCELLED = "cancelled", _("Cancelled")
        EXPIRED = "expired", _("Expired")

    tenant = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    plan = models.ForeignKey(
        "subscription.SubscriptionPlan",
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )

    status = models.CharField(
        _("status"),
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIALING,
    )

    current_period_start = models.DateTimeField(_("current period start"))
    current_period_end = models.DateTimeField(_("current period end"))

    trial_start = models.DateTimeField(_("trial start"), null=True, blank=True)
    trial_end = models.DateTimeField(_("trial end"), null=True, blank=True)

    cancel_at_period_end = models.BooleanField(_("cancel at period end"), default=False)
    cancelled_at = models.DateTimeField(_("cancelled at"), null=True, blank=True)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = SubscriptionManager()

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["current_period_start", "current_period_end"]),
        ]

    def __str__(self) -> str:
        return f"{self.tenant} - {self.plan}"

    @property
    def is_active(self) -> bool:
        if not self.current_period_start or not self.current_period_end:
            return False

        now = timezone.now()
        return (
            self.status in [
                self.SubscriptionStatus.TRIALING,
                self.SubscriptionStatus.ACTIVE,
            ]
            and self.current_period_start <= now <= self.current_period_end
        )


    @property
    def is_trial(self) -> bool:
        if not self.trial_start or not self.trial_end:
            return False

        now = timezone.now()
        return (
            self.status == self.SubscriptionStatus.TRIALING
            and self.trial_start <= now <= self.trial_end
        )