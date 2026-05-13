from __future__ import annotations

import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionPlanQuerySet",
    "SubscriptionPlanManager",
    "SubscriptionPlan",
)


class SubscriptionPlanQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


_SubscriptionPlanManagerBase = models.Manager.from_queryset(SubscriptionPlanQuerySet)


class SubscriptionPlanManager(_SubscriptionPlanManagerBase):
    pass


class SubscriptionPlan(get_subid_model()):
    """
    SaaS subscription plan.

    Example:
    - Starter
    - Pro
    - Business
    - Enterprise
    """

    class BillingInterval(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        YEARLY = "yearly", _("Yearly")

    name = models.CharField(_("name"), max_length=100)
    code = models.SlugField(_("code"), max_length=100, unique=True)

    description = models.TextField(_("description"), blank=True)

    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(_("currency"), max_length=10, default="IDR")

    billing_interval = models.CharField(
        _("billing interval"),
        max_length=20,
        choices=BillingInterval.choices,
        default=BillingInterval.MONTHLY,
    )

    # max_users = models.PositiveIntegerField(_("max users"), default=1)
    # max_events_per_month = models.PositiveIntegerField(_("max events per month"), default=10)

    is_active = models.BooleanField(_("is active"), default=True)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = SubscriptionPlanManager()

    class Meta:
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")
        ordering = ["price", "id"]

    def __str__(self) -> str:
        return self.name