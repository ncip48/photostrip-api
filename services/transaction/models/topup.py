from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

if TYPE_CHECKING:
    from services.account.models import User

logger = logging.getLogger(__name__)

__all__ = (
    "TopupTransactionQuerySet",
    "TopupTransactionManager",
    "TopupTransaction",
)


class TopupTransactionQuerySet(models.QuerySet):
    def owned(self, user: User) -> TopupTransactionQuerySet:
        return self.filter(user=user)


_TopupTransactionManagerBase = models.Manager.from_queryset(TopupTransactionQuerySet)


class TopupTransactionManager(_TopupTransactionManagerBase):
    pass


class TopupTransaction(get_subid_model()):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="topups"
    )
    reference = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="topups"
    )
    token = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    qris = models.TextField(max_length=100, null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provider = models.CharField(max_length=50)  # qris, paypal, midtrans
    created = models.DateTimeField(auto_now_add=True)

    objects = TopupTransactionManager()

    class Meta:
        verbose_name = _("topup transaction")
        verbose_name_plural = _("topup transactions")

    def __str__(self) -> str:
        return f"{self.user} ({self.pk})"
